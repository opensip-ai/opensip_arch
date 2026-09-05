#!/usr/bin/env python3
"""check-evaluation-proof-v12.py — executable checker for evaluation-proof.v12.json.

v12 is the successor to evaluation-proof.v11.json, which an independent reviewer
REJECTED (ep11.review-independent.json, 2 blocking findings: IR-EP11-01 and
IR-EP11-02).

============================================================================
THE ONE SENTENCE THAT MATTERS
============================================================================
v11's answer-provenance rule A-2 tagged a returned object by WHICH MODULE OBJECT
THE ATTRIBUTE WAS READ FROM, so a route region that installed its own serving
function on that attribute satisfied every rule while 7 of 7 pinned verdicts came
out of the superseded encoder.  v12 anchors provenance to the IDENTITY OF THE
FUNCTION OBJECT THAT THE VERIFIED BYTES DEFINED, captured from the guard's own
private instantiation of the pinned snapshot before any route-region code can
run, compared by `is`, and it separately measures that the installation the route
region is handed is still the one built at load time.

============================================================================
WHAT v12 DOES *NOT* CLAIM — read this before reading the green banner
============================================================================
RES-EP12-02 is the boundary and it is stated first because the banner is scoped
by it.  The answer-provenance property holds against a hostile ROUTE REGION.  It
does NOT hold against a route region that reads or writes THIS GUARD'S OWN STACK
FRAME, or the closure cells of the servers this guard installs.  That is not an
argument: variants AX6, AX9 and RX2c are BUILT, EXECUTED and MEASURED on every
ordinary run, they defeat every scored guard, and they are published in the
escaped set and printed in the banner.  The source tripwire that flags the cheap
spellings of that class is an ENUMERATION of identifiers; RX2c is spelled with
six it does not name and the tripwire is MEASURED to be blind to it on every run.
No property this instrument publishes rests on that enumeration.

Usage:
    python3 -I -B check-evaluation-proof-v12.py [artifact.json]
    python3 -I -B check-evaluation-proof-v12.py --selftest

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
BINDING = "evaluation-proof.v12.json"
EXPECTED_VERSION = 12
DECLARED_FLAGS = ("--selftest",)

MALFORMED = (TypeError, ValueError, KeyError, IndexError, AttributeError,
             ZeroDivisionError, OverflowError, RecursionError, UnicodeError,
             StopIteration)

EP11 = "check-evaluation-proof-v11.py"
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
EP11_ARTIFACT = "evaluation-proof.v11.json"
EP11_REVIEW = "ep11.review-independent.json"
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

# The REJECTED predecessor's own bytes.  v12 does NOT delegate to them and does
# NOT run their checking layer: v11 exits 0 on its own candidate while publishing
# a property this candidate retracts as false, so executing that layer would
# republish the retracted green.  They are pinned and EXECUTED for exactly one
# purpose: the predecessor-defeat control, which rebuilds the blocking evasion
# inside v11's own route region and MEASURES that v11's guard stays silent.
PREDECESSOR_INSTRUMENT = {
    EP11: "15ac67e249604f251c0ee116a7a397db1b4a445c24bc313b76c77e08908f822e",
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
    EP11_ARTIFACT: "9a31241ee4f1f6b72712a126453e2467359d1c07c4b658db1b699f6500a31f5a",
    EP11_REVIEW: "209ff0e14eba88eca1bdd3d96befc3251cbaa4919405ebc691530d90b4140000",
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

ALL_PINS = {**DELEGATED_CHECKER, **PREDECESSOR_INSTRUMENT, **DELEGATION_CLOSURE,
            **SUPERSEDED_ENCODER, **PINNED_DATA}

# The vector source is evaluation-proof.v8.json, which carries a PASSING
# independent review.  v9, v10 and v11 are REJECTED, so v12 takes no vector
# authority from any of them; all are pinned, parsed, and v9 is required to AGREE
# with EP8.
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
# verification and execution for anything v12 loads.
#
# Stated so the rule is not over-read, because predecessors do re-read:
#   * check-evaluation-proof-v10.py's and check-evaluation-proof-v11.py's own
#     _own_source() would re-open their own paths to feed their AST scans and
#     their evasion batteries.  v12 seeds BOTH caches with the VERIFIED bytes
#     before any of it runs, so neither re-reads.  Enforced and measured
#     (delegateSourceCacheSeeded, predecessorSourceCacheSeeded).
#   * EP6.admit_evaluation_authority re-reads c2-plan-stage-schema.v3.json and
#     fact-plane.v1.json on every call, and EP8._ep7 sha_file()-verifies then
#     loads from disk.  Both hash-verify what they re-read, so the trust order
#     holds transitively, but the guarantee v12 makes is about what v12 loads.
#   * v12's own bytes are, by construction, not in v12's own pinned set
#     (RES-EP12-05), and _own_source() reads them from disk for the tripwires.
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


def _exec_verified(filename: str, source: bytes, prefix: str = "_ep12"):
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


def _private_module(snapshots, name: str, prefix: str):
    """A private instance of a pinned module, re-verified rather than trusted.

    If the snapshot the guard was handed does not hash to the pin, the guard
    refuses instead of measuring against whatever it was given.
    """
    source = snapshots[name]
    if sha_bytes(source) != ALL_PINS[name]:
        raise AuthorityLoadError(
            f"the {name} bytes handed to the answer-provenance guard hash to "
            f"{sha_bytes(source)}, pinned at {ALL_PINS[name]}")
    return _exec_verified(name, source, prefix=prefix)


# --------------------------------------------------------------------------
# Section 1.  Delegation to the checker two versions back, whose measurements an
# independent reviewer verified by re-execution.
#
# ep10.review-independent.json UPHELD v10's two-regime admitted-set measurement,
# its admissionDescriptor finding, its differential oracle, its distinct-intent
# family, its probe family and its call ledger; ep11.review-independent.json
# re-verified every one of them by executing v10 itself and reported them
# reproduced digit for digit.  v12 must not regress or rebuild any of them, so it
# does neither: it hash-verifies check-evaluation-proof-v10.py and EXECUTES the
# reviewer-verified measurement functions from that verified snapshot, and drives
# the pinned v10 candidate through v10's OWN checking layer requiring zero
# findings.  Nothing is transcribed.
#
# v11 is deliberately NOT delegated to.  Its own checking layer exits 0 on its
# own candidate while that candidate publishes the answer-provenance property
# RET-EP12-01 retracts as false; running that layer here would republish a green
# this candidate exists to withdraw.  v11's bytes are pinned and executed only by
# the predecessor-defeat control in Section 8.
# --------------------------------------------------------------------------

def load_delegate(snapshots: dict[str, bytes]):
    delegate = _exec_verified(EP10, snapshots[EP10], prefix="_ep12_delegate")
    # Trust order: the delegate's self-scan cache is seeded with the VERIFIED
    # bytes so its AST scans and its evasion battery never re-open the path.
    delegate._SCAN_CACHE["source"] = snapshots[EP10]
    delegate._SCAN_CACHE["tree"] = ast.parse(snapshots[EP10])
    return delegate


def delegate_source_is_sealed(delegate, snapshots) -> bool:
    """MEASURED: the delegate's self-source cache holds the verified bytes."""
    return delegate._SCAN_CACHE.get("source") == snapshots[EP10]


class Authority:
    """v12's authority: the delegate's Authority plus v12's own verified bytes.

    The route region receives THIS object.  Stated accurately, because
    ep11.review-independent.json IR-EP11-NB-06 found the predecessor's version of
    this docstring false in its own bytes: this object DOES carry the verified
    snapshot dictionary as self._snapshots, and the inner v10 Authority carries
    it as self.snapshots, so a route region can read every verified byte string
    by plain attribute access and can build its own instance of the repaired
    module from them with no introspection at all.  That is deliberate and it
    does not defeat anything here: an instance the route region builds is NOT the
    function object this guard anchors on, and A-2 compares by identity, not by
    provenance-of-the-bytes.  What this object does NOT carry is the guard's
    private instances, its anchors or its witness; those exist only in the
    guard's frame, and reaching them is the declared boundary RES-EP12-02.
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
# Each function returns the served module's OWN result object rather than a fresh
# copy of it: a copy is a different object and no identity rule could bind it.
# Totality is preserved by the boundary handler, not by copying.
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
                          "injection_isolation_probe", "_sentinel_for")


def c2_join(intent, authority):
    """The complete v12 authority join over one PlanIntent.

    Returns the three values the checker ACTS ON, always, including when the
    verdict is a rejection, because the accept / reject gate IS the validation
    verdict and LB-C2-01 lives exactly there.
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
            findings.append(f"EP12-C2-API: {C2V4} does not expose a callable {name}")
            continue
        original = authority.ledger.originals.get((C2V4, name), function)
        try:
            arity = original.__code__.co_argcount
        except AttributeError:
            findings.append(f"EP12-C2-API: {name} in {C2V4} is not a plain function")
            continue
        expected = 3 if name == "validate_plan_intent" else 2
        if arity != expected:
            findings.append(f"EP12-C2-API: {C2V4}.{name} takes {arity} positional "
                            f"parameters; the imported seam requires {expected}")
    return findings


# --------------------------------------------------------------------------
# Section 3.  CALL provenance — v10's ledger rules, restated for what they show.
#
# WHAT THEY ESTABLISH, stated plainly and not one word more: that the calls the
# join MADE for each pinned vector went into the repaired module.  They do NOT
# establish that the value the join RETURNED came out of it.  A call can be made
# correctly and its result discarded; that is evasion AX2 and every one of these
# rules is green while it runs.  Answer provenance is Section 4's job.
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
                f"EP12-CALL: vector {vector_id} produced ZERO observed C-2 calls; "
                "the authority join reached a C-2 API by a route the served-module "
                "ledger cannot observe, or made no call at all")
        if tags and tags != [C2V4]:
            findings.append(
                f"EP12-CALL: vector {vector_id}'s authority join was served by "
                f"{tags}; the C-2 join is re-pinned onto {C2V4} and EVERY call for "
                "a pinned vector must be served by the repaired module")
        if mismatched:
            findings.append(
                f"EP12-CALL: vector {vector_id} observed {len(mismatched)} depth-0 "
                "C-2 call(s) over an argument that is NOT this vector's PlanIntent")
        if entries and apis != sorted(C2_IMPORTED_APIS):
            findings.append(
                f"EP12-CALL: vector {vector_id} exercised depth-0 APIs {apis}; all "
                f"three of {sorted(C2_IMPORTED_APIS)} must be served for every "
                "pinned vector or the join is only partly re-pinned")
        if answer["gate"] != "ACCEPT":
            findings.append(
                "EP12-STABILITY: the C-2 join does not accept pinned vector "
                f"{vector_id}: {answer['verdict'][:1]}")
        rows.append({"vectorId": vector_id, "observedCalls": len(entries),
                     "depthZeroCalls": len(outer), "servedBy": tags, "apis": apis,
                     "argumentBound": not mismatched, "gate": answer["gate"]})

    driven = {value_fingerprint(intent) for _id, intent in named_intents}
    if len(observed) != len(driven):
        findings.append(
            f"EP12-CALL: {len(observed)} distinct PlanIntent fingerprint(s) were "
            f"observed at depth 0, but the driven vectors carry {len(driven)}")
    if superseded_calls:
        findings.append(f"EP12-CALL: {superseded_calls} superseded-module call(s) "
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
# Section 4.  ANSWER provenance — the repair of IR-EP11-01.
#
# WHAT WENT WRONG IN THE PREDECESSOR, precisely.  v11's witness wrapper derived
# the tag it recorded from WHICH MODULE OBJECT the attribute was read from at
# window entry:
#
#     current = getattr(module, api)                      # v11
#     setattr(module, api, _witness_wrapper(w, current, tag, api))
#
# `tag` was therefore a property of the SEAT, and _poisoned wrote to that same
# seat.  A route region that assigned its own serving function to
# authority.c2v4().validate_plan_intent before the window opened had all three of
# A-2, A-3 and A-4 anchored to one binding IT owned, reached through the DECLARED
# accessor with no introspection of any kind.  Rebuilt here as variant
# RX1-seat-substitution-declared-accessor, and MEASURED against v11's own bytes
# by the predecessor-defeat control in Section 8.
#
# THE ANCHOR v12 USES INSTEAD, stated exactly so it can be attacked.
#
#   The anchor is the FUNCTION OBJECT that the verified bytes defined:
#   getattr(instance, api) where `instance` is a module object this guard creates
#   by executing the SHA-256-verified snapshot of check-c2-v4.py inside this
#   function, read at the instant that execution returns, before any route-region
#   code has run against it.  It is held in a local of answer_provenance_guard
#   and in the closure of the servers this guard installs.  It is never assigned
#   to a module global, never stored on the Authority, never returned, and never
#   passed to the route region.  A-2 compares by `is` against that local.
#
#   WHY THE ROUTE REGION CANNOT REBIND IT.  A seat is a binding; an anchor is an
#   object.  The region can write any binding it can name — and it is expected
#   to; A-6 measures exactly that — but writing a binding does not change which
#   object this guard's local names.  The server records THE CALLEE IT ACTUALLY
#   INVOKED, read out of its own cell at call time:
#
#       callee = anchor            # cell read
#       result = callee(*args)     # the object that produced the answer
#       record(callee, ...)        # what was really called, not what should be
#
#   so even a rewritten closure cell is reported rather than believed: the record
#   then carries the substitute and `record.callee is anchors[api]` is False.
#
#   WHAT REMAINS POSSIBLE, measured rather than denied.  A route region that
#   reads or writes this guard's own stack frame, or the closure cells of these
#   servers, reaches `anchors` and `witness` themselves and can overwrite an
#   honest record's result field.  Variants AX6, AX9 and RX2c do exactly that,
#   are executed on every ordinary run, and are MEASURED to defeat every scored
#   guard.  They are published in escapedEveryGuard and printed in the banner.
#   That is the declared scope RES-EP12-02, and nothing published here is true
#   only because a source scan failed to find a spelling.
#
# EIGHT RULES, each stating what it establishes and what it does not:
#
#   A-1  INDEPENDENT VALUE.  A SECOND private instance of check-c2-v4.py — not
#        the anchored one — computes the three answers over a private deep copy
#        of the PlanIntent, a private parse of the pinned contract and a private
#        relation set.  The join's answers must equal them TYPE-EXACTLY.
#        Establishes: the VALUE is the repaired instrument's value, agreed by two
#        independent instantiations of the same verified bytes.
#        Does not establish: that the value came FROM either of them.
#
#   A-2  ANCHORED OBJECT PROVENANCE.  Each returned value must BE, by object
#        identity, the result of a call this guard's server made INTO THE ANCHOR,
#        at depth 0, over this vector's PlanIntent fingerprint, inside this
#        vector's anchored window, with the recorded callee identical to the
#        anchor.
#        Establishes: the object the join returned is the object the verified
#        bytes produced for this input.
#        Does not establish: anything about the object's CONTENT — a region that
#        returns the anchor's own list after appending to it satisfies A-2 and
#        fails A-1.
#
#   A-3  SENTINEL FLOW, repaired module poisoned.  Every reachable spelling of
#        the repaired module's api — every module object the authority exposes
#        AND the ledger's unwrapped original — is replaced by a function
#        returning a per-run UNPREDICTABLE sentinel, and the join is driven again
#        WITHOUT the anchored install.  The answer must BECOME the sentinel.
#        Establishes: CAUSAL DEPENDENCE on the declared route.
#
#   A-4  SENTINEL FLOW, superseded module poisoned.  Symmetrically; the answer
#        must be UNCHANGED and must still equal A-1's independent value.
#        Establishes: NON-dependence on the superseded module.
#
#   A-5  THE GATE.  The accept / reject gate must be the gate the independent
#        instance decides.  Stated separately because c2_join returns early on
#        any finding, so a verdict substitution decides admission by itself.
#
#   A-6  INSTALLATION INTEGRITY.  Before the unanchored window, after it, and
#        after the anchored window, the two module objects the authority exposes,
#        the objects bound at their three seats, the ledger object, the ledger's
#        unwrapped originals and the objects the two declared accessors return
#        must all be IDENTICAL — by `is` — to the ones captured at load time,
#        before any route-region code ran; and the anchored server must still be
#        at its seat when the anchored window closes.
#        Establishes: no declared accessor's target was rebound, replaced,
#        wrapped or displaced.  This is what catches RX1: v11's guard was green
#        for it because the guard read the seat; this rule reads the seat and
#        compares it with what was installed.
#        Does not establish: anything about a region that rebinds and restores
#        entirely between two checks — that case is A-2's, because the object it
#        returns was not produced by the anchor.
#
#   A-7  UNANCHORED AGREEMENT.  The join is ALSO driven with the real
#        installation untouched, and that answer must equal A-1's independent
#        value TYPE-EXACTLY.  The shared served-module ledger's own agreement is
#        measured beside it and published but is NOT a rule: the shared ledger is
#        reachable from the route region and can be told a call happened that did
#        not.
#        Establishes: the anchored install did not change the subject's answer.
#        Does not establish: object provenance outside the anchored window — that
#        is RES-EP12-16 and it is a real residual of this design.
#
#   A-8  AGGREGATE AND ANCHOR INTEGRITY, measured and published: per-rule counts;
#        the anchor objects and their code objects unchanged across the drive;
#        the anchored instance's own function bindings unchanged across the
#        drive; exactly one anchored record per api per window, all at depth 0,
#        all against the repaired tag, all over this vector's fingerprint; and
#        zero unevaluated rules — a rule that could not be evaluated is a
#        finding, not an omission.
#
# WHAT NONE OF THIS ESTABLISHES.  Provenance is not correctness: if
# check-c2-v4.py is itself wrong, A-1..A-8 certify that its wrong answer is
# faithfully the one used.  RES-EP12-15 records that C-2 v4's own published
# self-census is under a BLOCKING adjudication today.
# --------------------------------------------------------------------------

class _WitnessRecord:
    """One call this guard's own server made, recorded by what it CALLED."""

    __slots__ = ("callee", "tag", "api", "argfp", "depth", "result")

    def __init__(self, callee, tag, api, argfp, depth, result):
        self.callee = callee
        self.tag = tag
        self.api = api
        self.argfp = argfp
        self.depth = depth
        self.result = result


class _Witness:
    """A PRIVATE append-only record, created inside answer_provenance_guard.

    Bound to no global and to no attribute of anything the route region receives.
    Reaching it requires this guard's frame or a server's closure cell, which is
    the declared boundary RES-EP12-02 and is MEASURED by AX6, AX9 and RX2c.
    """

    __slots__ = ("records", "depth")

    def __init__(self):
        self.records: list[_WitnessRecord] = []
        self.depth = 0


def _anchored_server(witness, anchor, tag, api):
    """A server whose callee is fixed by CLOSURE, and which records what it called.

    `anchor` is the function object the verified bytes defined.  It is read out
    of the cell into a local before the call, the local is what is invoked, and
    the local is what is recorded — so a rewritten cell produces a record that
    names the substitute rather than a record that lies about it.
    """
    def served(*args, **kwargs):
        callee = anchor
        depth = witness.depth
        witness.depth += 1
        try:
            result = callee(*args, **kwargs)
        finally:
            witness.depth -= 1
        witness.records.append(_WitnessRecord(
            callee, tag, api, value_fingerprint(args[0]) if args else None,
            depth, result))
        return result
    return served


@contextlib.contextmanager
def _anchored(witness, targets):
    """Install this guard's own anchored servers at every reachable spelling.

    `targets` is a sequence of (tag, modules, anchors).  On exit the servers are
    required to still be where they were put — a region that displaces one is
    reported, not silently restored over.
    """
    installed = []
    for tag, modules, anchors in targets:
        for api in C2_IMPORTED_APIS:
            anchor = anchors.get(api)
            if anchor is None:
                continue
            served = _anchored_server(witness, anchor, tag, api)
            for module in modules:
                try:
                    saved = getattr(module, api)
                    setattr(module, api, served)
                except MALFORMED:
                    continue
                installed.append((module, api, served, saved))
    state = {"heldAtExit": True, "displaced": []}
    try:
        yield state
    finally:
        for module, api, served, saved in installed:
            if getattr(module, api, None) is not served:
                state["heldAtExit"] = False
                state["displaced"].append(
                    f"{getattr(module, '__name__', type(module).__name__)}.{api}")
            try:
                setattr(module, api, saved)
            except MALFORMED:
                continue
        state["displaced"] = sorted(set(state["displaced"]))


def _sentinel_for(api: str, token: str):
    """A value of the api's own shape that the repaired module cannot produce."""
    if api == "validate_plan_intent":
        return [("EP12-SENTINEL", token)]
    if api == "plan_intent_commitment":
        return "sha256:" + token
    return b"EP12-SENTINEL\x00" + token.encode("utf-8")


@contextlib.contextmanager
def _poisoned(modules, ledger, tag, api, value):
    """Replace EVERY reachable spelling of api on every given module object."""
    def sentinel(*_args, **_kwargs):
        return value

    saved = []
    for module in modules:
        try:
            prior = getattr(module, api)
        except MALFORMED:
            continue
        try:
            setattr(module, api, sentinel)
        except MALFORMED:
            continue
        saved.append((module, prior))
    had_original = (tag, api) in ledger.originals
    saved_original = ledger.originals.get((tag, api))
    if had_original:
        ledger.originals[(tag, api)] = sentinel
    try:
        yield
    finally:
        for module, prior in saved:
            try:
                setattr(module, api, prior)
            except MALFORMED:
                continue
        if had_original:
            ledger.originals[(tag, api)] = saved_original


def reachable_modules(authority, installation, tag):
    """Every distinct object the authority exposes for one C-2 tag."""
    found = []
    candidates = [installation["rows"][tag]["module"]]
    try:
        candidates.append(authority.module(tag))
    except MALFORMED:
        pass
    try:
        candidates.append(authority.c2v4() if tag == C2V4 else authority.c2v3())
    except MALFORMED:
        pass
    for item in candidates:
        if item is None:
            continue
        if not any(item is seen for seen in found):
            found.append(item)
    return found


def _code_fingerprint(function):
    """A behavioural fingerprint of the CODE a served function actually runs.

    Two module objects executed from the same verified byte string hold two
    DIFFERENT function objects, so identity cannot relate them; the code they
    run is the same and this fingerprints it.  ep11.review-independent.json named
    exactly this as the shape of the repair: a behavioural fingerprint of the
    served module, not a source scan.
    """
    code = getattr(function, "__code__", None)
    if code is None:
        return None
    return sha_bytes(canonical([
        code.co_name, code.co_argcount, code.co_kwonlyargcount, code.co_flags,
        list(code.co_varnames), list(code.co_names), code.co_code.hex()]))


def capture_installation(authority):
    """The load-time installation, captured BEFORE any route-region code runs.

    This object is a LOCAL of the caller and is threaded to the guards by
    parameter.  It is never bound to a module global and never stored on the
    Authority, because the route region's globals ARE this module's globals: a
    module-level table would be writable from the region by plain name.
    """
    rows = {}
    defects = []
    for tag in (C2V4, C2V3):
        try:
            module = authority.module(tag)
        except MALFORMED:
            module = None
        try:
            accessor = authority.c2v4() if tag == C2V4 else authority.c2v3()
        except MALFORMED:
            accessor = None
        seats, originals, fingerprints = {}, {}, {}
        for api in C2_IMPORTED_APIS:
            seats[api] = getattr(module, api, None)
            originals[api] = authority.ledger.originals.get((tag, api))
            fingerprints[api] = _code_fingerprint(originals[api])
            marker = getattr(seats[api], "__ledger_tag__", None)
            if marker != tag:
                defects.append(
                    f"{tag}.{api} was not the served-module ledger's own wrapper "
                    "at the moment this run captured the installation")
        rows[tag] = {"module": module, "accessor": accessor, "seats": seats,
                     "originals": originals, "fingerprints": fingerprints}
    return {"rows": rows, "ledger": authority.ledger,
            "capturedClean": not defects, "captureDefects": sorted(set(defects))}


def installation_status(installation, authority) -> list[str]:
    """MEASURED, reading no source: is the installation still the one installed?"""
    defects: list[str] = []
    if authority.ledger is not installation["ledger"]:
        defects.append("the served-module ledger object was replaced")
    for tag in (C2V4, C2V3):
        row = installation["rows"][tag]
        try:
            module = authority.module(tag)
        except MALFORMED:
            module = None
        if module is not row["module"]:
            defects.append(f"authority.module({tag}) is no longer the module object "
                           "instrumented at load time")
        try:
            accessor = authority.c2v4() if tag == C2V4 else authority.c2v3()
        except MALFORMED:
            accessor = None
        if accessor is not row["accessor"]:
            defects.append(f"the declared accessor for {tag} no longer returns the "
                           "module object instrumented at load time")
        for api in C2_IMPORTED_APIS:
            if getattr(row["module"], api, None) is not row["seats"][api]:
                defects.append(f"{tag}.{api} is no longer the ledger wrapper "
                               "installed at load time")
            if authority.ledger.originals.get((tag, api)) is not row["originals"][api]:
                defects.append(f"the ledger's unwrapped original for {tag}.{api} "
                               "was replaced")
    return sorted(set(defects))


def restore_installation(installation, authority) -> None:
    """Put the load-time installation back.

    The GUARD never does this between its own checks — hiding a rebinding is the
    opposite of measuring it.  The harness does it AFTER a hostile configuration
    has been scored, so that one variant's persistent write cannot silently move
    the next variant's numbers.
    """
    for tag in (C2V4, C2V3):
        row = installation["rows"][tag]
        for api in C2_IMPORTED_APIS:
            if row["seats"][api] is not None:
                try:
                    setattr(row["module"], api, row["seats"][api])
                except MALFORMED:
                    continue
            if row["originals"][api] is not None:
                installation["ledger"].originals[(tag, api)] = row["originals"][api]


def _function_bindings(module) -> dict[str, int]:
    return {name: id(value) for name, value in vars(module).items()
            if isinstance(value, types.FunctionType)}


def answer_provenance_guard(named_intents, authority, snapshots, installation):
    findings: list[str] = []
    rows: list[dict[str, Any]] = []
    counts = {"vectors": 0, "apisPerVector": len(ANSWER_KEYS),
              "independentValueAgreements": 0, "anchoredObjectAgreements": 0,
              "sharedLedgerAgreements": 0,
              "repairedSentinelFlowed": 0, "supersededSentinelIgnored": 0,
              "gateAgreements": 0, "installationIntact": 0,
              "unanchoredValueAgreements": 0, "recordParityHeld": 0,
              "evaluationErrors": 0}
    try:
        anchor_instance = _private_module(snapshots, C2V4, "_ep12_anchor")
        anchors = {api: getattr(anchor_instance, api) for api in C2_IMPORTED_APIS}
        anchor_code = {api: anchors[api].__code__ for api in C2_IMPORTED_APIS}
        anchor_bindings = _function_bindings(anchor_instance)
        superseded_instance = _private_module(snapshots, C2V3, "_ep12_anchor3")
        superseded_anchors = {api: getattr(superseded_instance, api)
                              for api in C2_IMPORTED_APIS}
        reference = _private_module(snapshots, C2V4, "_ep12_reference")
        contract = json.loads(snapshots[C2V4_CONTRACT].decode("utf-8"),
                              object_pairs_hook=_pairs)
        relations = set(json.loads(snapshots[FACT_PLANE].decode("utf-8"),
                                   object_pairs_hook=_pairs)
                        ["relationRegistry"]["relations"])
    except (AuthorityLoadError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError, *MALFORMED) as exc:
        return ([f"EP12-ANSWER: the guard could not build its anchored and "
                 f"reference instances: {type(exc).__name__}: {exc}"], counts, rows)

    for api in C2_IMPORTED_APIS:
        if not isinstance(anchors[api], types.FunctionType):
            findings.append(
                f"EP12-ANSWER: {C2V4}.{api} is not a plain function in a freshly "
                "executed instance of the verified bytes; there is nothing to "
                "anchor on")

    # A-6, the half that no identity comparison can reach: the function the
    # ledger will actually call must be running the CODE the verified bytes
    # define.  A seat rebound BEFORE this run captured anything carries the
    # ledger's own markers and is identical to itself ever after; what it cannot
    # do is run check-c2-v4.py's code while serving check-c2.py's answers.
    served_defects = []
    for tag, anchor_map in ((C2V4, anchors), (C2V3, superseded_anchors)):
        for api in C2_IMPORTED_APIS:
            if installation["rows"][tag]["fingerprints"].get(api) != \
                    _code_fingerprint(anchor_map[api]):
                served_defects.append(
                    f"the ledger's unwrapped original for {tag}.{api} does not run "
                    f"the code the SHA-256-verified bytes of {tag} define")
    served_defects = sorted(set(served_defects))

    ledger = authority.ledger
    witness = _Witness()
    if not installation["capturedClean"]:
        findings.append(
            "EP12-ANSWER: the served-module installation was ALREADY not the "
            "ledger's own at the moment this run captured it: "
            f"{installation['captureDefects']} (A-6)")

    for vector_id, intent in named_intents:
        counts["vectors"] += 1
        want = value_fingerprint(intent)
        subject = copy.deepcopy(intent)
        repaired_modules = reachable_modules(authority, installation, C2V4)
        superseded_modules = reachable_modules(authority, installation, C2V3)

        # A-6, first half: the installation as the region left it.
        before = installation_status(installation, authority)

        # A-7's drive: the REAL installation, untouched.
        with ledger.window(f"answer-unanchored:{vector_id}") as ledger_window:
            unanchored = c2_join(intent, authority)
        ledger_entries = ledger_window.entries
        middle = installation_status(installation, authority)

        # A-2's drive: this guard's own servers, whose callee is the anchor.
        low = len(witness.records)
        targets = [(C2V4, repaired_modules, anchors),
                   (C2V3, superseded_modules, superseded_anchors)]
        with _anchored(witness, targets) as anchored_state:
            answer = c2_join(intent, authority)
        high = len(witness.records)
        after = installation_status(installation, authority)
        window_records = witness.records[low:high]

        defects = sorted(set(before) | set(middle) | set(after)
                         | set(served_defects))
        if not anchored_state["heldAtExit"]:
            defects.append("this guard's anchored server was displaced from "
                           f"{anchored_state['displaced']} before the window closed")
        row = {"vectorId": vector_id, "gate": answer["gate"],
               "installationDefects": defects, "perApi": {}}
        if defects:
            findings.append(
                f"EP12-ANSWER: vector {vector_id}: the served-module installation "
                f"this run captured at load time no longer holds: {defects} (A-6). "
                "A binding the route region can write is not an anchor, and a "
                "guard that reads the seat to decide provenance is measuring "
                "whatever the region put there")
        else:
            counts["installationIntact"] += 1

        # A-1's reference values, computed AFTER the drives on a SECOND private
        # instance, from private copies.  Nothing the route region can reach
        # carries these values while the route region is running: they do not
        # exist yet.
        try:
            expected = {
                "verdict": reference.validate_plan_intent(
                    subject, copy.deepcopy(contract), set(relations)),
                "commitment": reference.plan_intent_commitment(
                    subject, copy.deepcopy(contract)),
                "preimage": reference.canonical_plan_intent(
                    subject, copy.deepcopy(contract)),
            }
        except MALFORMED as exc:
            counts["evaluationErrors"] += 1
            findings.append(
                f"EP12-ANSWER: the independent reference instance raised on pinned "
                f"vector {vector_id}: {type(exc).__name__}: {exc}")
            rows.append(row)
            continue
        expected_gate = "ACCEPT" if not expected["verdict"] else "REJECT"
        row["expectedGate"] = expected_gate

        # A-5, stated first because it is the one that decides admission.
        if answer["gate"] != expected_gate:
            findings.append(
                f"EP12-ANSWER: vector {vector_id} the join's accept/reject GATE is "
                f"{answer['gate']}; the independently computed repaired instance "
                f"decides {expected_gate}. The gate IS the validation verdict, and "
                "LB-C2-01 lives exactly there (A-5)")
        else:
            counts["gateAgreements"] += 1
        if expected_gate != "ACCEPT":
            findings.append(
                "EP12-STABILITY: the repaired C-2 instrument does not accept pinned "
                f"vector {vector_id}")

        # A-8's record parity for this window.
        parity = (len(window_records) == len(ANSWER_KEYS)
                  and all(entry.tag == C2V4 and entry.depth == 0
                          and entry.argfp == want
                          and entry.callee is anchors.get(entry.api)
                          for entry in window_records)
                  and sorted(entry.api for entry in window_records)
                  == sorted(C2_IMPORTED_APIS))
        row["anchoredRecords"] = len(window_records)
        if parity:
            counts["recordParityHeld"] += 1
        else:
            findings.append(
                f"EP12-ANSWER: vector {vector_id}: the anchored window recorded "
                f"{len(window_records)} call(s) into the anchor; exactly one per "
                "imported API at depth 0 over this vector's PlanIntent is required "
                "(A-8). A window that reaches the anchor by another route, or that "
                "reaches it for another argument, is not measuring this vector")

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
                    f"EP12-ANSWER: vector {vector_id} {key}: the value the join "
                    "returned is not the value an independent instance of the "
                    "verified repaired bytes computed for this PlanIntent (A-1)")

            # A-2 ANCHORED object provenance.  The record is located by object
            # identity inside THIS window's slice; the identity that matters is
            # `witnessed.callee is anchors[api]`, which is this guard's own frame
            # local holding the function object the verified bytes defined.
            witnessed = None
            if actual is not None:
                for item in window_records:
                    if item.result is actual:
                        witnessed = item
                        break
            per["anchoredObject"] = bool(
                witnessed is not None
                and witnessed.callee is anchors.get(api)
                and witnessed.tag == C2V4 and witnessed.api == api
                and witnessed.argfp == want and witnessed.depth == 0)
            per["sharedLedgerAgrees"] = unanchored[key] is not None and any(
                entry.tag == C2V4 and entry.depth == 0 and entry.api == api
                and entry.argfp == want and entry.result is unanchored[key]
                for entry in ledger_entries)
            if per["sharedLedgerAgrees"]:
                counts["sharedLedgerAgreements"] += 1
            if per["anchoredObject"]:
                counts["anchoredObjectAgreements"] += 1
            else:
                findings.append(
                    f"EP12-ANSWER: vector {vector_id} {key}: the object the join "
                    "returned is not an object THIS GUARD'S ANCHOR produced for "
                    "this vector's PlanIntent at depth 0 in this window (A-2). The "
                    "anchor is the function object the SHA-256-verified bytes of "
                    f"{C2V4} defined, captured in this guard's frame before any "
                    "route-region code ran; a call whose result is discarded, an "
                    "answer taken from another instrument, an object obtained for "
                    "a different argument and a forged ledger entry all fail here")

            # A-7 the unanchored answer.
            per["unanchoredValue"] = strict_equal(unanchored[key], expected[key])
            if per["unanchoredValue"]:
                counts["unanchoredValueAgreements"] += 1
            else:
                findings.append(
                    f"EP12-ANSWER: vector {vector_id} {key}: with this guard's "
                    "anchored servers NOT installed, the join returned a different "
                    "value from the independent reference instance (A-7); the "
                    "measurement and the unobserved behaviour disagree")

            # A-3 sentinel flow: the repaired module is poisoned and the answer
            # must follow it.  Driven WITHOUT the anchored install, so this is a
            # statement about the declared route, not about the guard's own.
            try:
                with _poisoned(repaired_modules, ledger, C2V4, api, sentinel):
                    poisoned_answer = c2_join(intent, authority)
                per["repairedSentinelFlowed"] = strict_equal(
                    poisoned_answer[key], sentinel)
            except Exception as exc:  # noqa: BLE001
                counts["evaluationErrors"] += 1
                per["repairedSentinelFlowed"] = False
                findings.append(f"EP12-ANSWER: vector {vector_id} {key}: A-3 could "
                                f"not be evaluated: {type(exc).__name__}: {exc}")
            if per["repairedSentinelFlowed"]:
                counts["repairedSentinelFlowed"] += 1
            else:
                findings.append(
                    f"EP12-ANSWER: vector {vector_id} {key}: with EVERY reachable "
                    f"spelling of {C2V4}.{api} replaced by a sentinel, the join "
                    "still returned an answer that is not the sentinel (A-3); the "
                    "answer does not FLOW FROM the repaired module, whatever the "
                    "call ledger recorded")

            # A-4 the superseded module is poisoned and the answer must not move.
            try:
                with _poisoned(superseded_modules, ledger, C2V3, api,
                               _sentinel_for(api, secrets.token_hex(16))):
                    unaffected = c2_join(intent, authority)
                per["supersededSentinelIgnored"] = strict_equal(
                    unaffected[key], expected[key])
            except Exception as exc:  # noqa: BLE001
                counts["evaluationErrors"] += 1
                per["supersededSentinelIgnored"] = False
                findings.append(f"EP12-ANSWER: vector {vector_id} {key}: A-4 could "
                                f"not be evaluated: {type(exc).__name__}: {exc}")
            if per["supersededSentinelIgnored"]:
                counts["supersededSentinelIgnored"] += 1
            else:
                findings.append(
                    f"EP12-ANSWER: vector {vector_id} {key}: with every reachable "
                    f"spelling of {C2V3}.{api} replaced by a sentinel, the join's "
                    "answer CHANGED (A-4); the answer flows from the superseded "
                    "module")
            row["perApi"][key] = per
        rows.append(row)

    # A-8's anchor integrity, re-read from this guard's own locals after the
    # whole drive.  A region that rewrote a server's cell, or the anchor's code
    # object, or a binding inside the anchored instance, is reported here without
    # reading a single byte of source.
    moved_anchors = sorted(
        api for api in C2_IMPORTED_APIS
        if getattr(anchor_instance, api, None) is not anchors[api]
        or getattr(anchors[api], "__code__", None) is not anchor_code[api])
    moved_bindings = sorted(
        name for name, ident in anchor_bindings.items()
        if id(vars(anchor_instance).get(name)) != ident)
    counts["anchorsUnmoved"] = not moved_anchors
    counts["anchorInstanceBindingsUnmoved"] = not moved_bindings
    if moved_anchors:
        findings.append(f"EP12-ANSWER: the anchor object or its code object moved "
                        f"for {moved_anchors} across the drive (A-8)")
    if moved_bindings:
        findings.append(f"EP12-ANSWER: function binding(s) {moved_bindings} inside "
                        "the anchored instance of the repaired module moved across "
                        "the drive (A-8)")

    if counts["evaluationErrors"]:
        findings.append(f"EP12-ANSWER: {counts['evaluationErrors']} answer-"
                        "provenance rule(s) could not be evaluated; an unevaluated "
                        "rule is a finding, not an omission")
    expected_total = counts["vectors"] * len(ANSWER_KEYS)
    counts["expectedPerRuleTotal"] = expected_total
    counts["allRulesHeld"] = (
        expected_total > 0
        and counts["independentValueAgreements"] == expected_total
        and counts["anchoredObjectAgreements"] == expected_total
        and counts["repairedSentinelFlowed"] == expected_total
        and counts["supersededSentinelIgnored"] == expected_total
        and counts["unanchoredValueAgreements"] == expected_total
        and counts["gateAgreements"] == counts["vectors"]
        and counts["installationIntact"] == counts["vectors"]
        and counts["recordParityHeld"] == counts["vectors"]
        and counts["anchorsUnmoved"]
        and counts["anchorInstanceBindingsUnmoved"]
        and not counts["evaluationErrors"])
    return findings, counts, rows


# --------------------------------------------------------------------------
# Section 5.  The differential oracle over the live census, RETAINED.
#
# v10's oracle is preserved by delegation and its numbers are republished.  This
# is v12's own instrument over v12's join, and it does two jobs v10's could not:
#   * it computes the repaired answer on a PRIVATE instance rather than through
#     the Authority, so a route region that poisons the reachable module cannot
#     poison the oracle's reference answer as well; and
#   * it ENUMERATES the silently-accepted positions instead of counting them.
#     IR-EP10-NB-03: a count is not a record.
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

MUTABLE_HOSTILE_LABELS = ("json-empty-object", "json-empty-array",
                          "json-deep-array", "json-object-leaf")


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

    A shared mutable injection-table member would make every surface count
    order-dependent if any guard mutated what it is handed.  RES-EP12-13 records
    the structural hazard and injection_isolation_probe MEASURES the premise on
    this run rather than asserting a consequence.
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
    """v12's differential oracle AND the plan-intent silent-accept enumeration."""
    stats = {"enumeratedCases": 0, "noOpInjections": 0, "executedCases": 0,
             "guardedEscapes": 0, "joinVsRepairedMismatches": 0,
             "supersededDivergentPositions": 0, "silentAccepts": 0}
    mismatches: list[str] = []
    divergent: list[str] = []
    silent: list[str] = []
    census, paths = node_census(intent)
    try:
        private = _private_module(snapshots, C2V4, "_ep12_oracle")
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
        findings.append("EP12-DIFF: the differential oracle could not run: "
                        f"{result['error']}")
    if result["stats"]["joinVsRepairedMismatches"]:
        findings.append(
            "EP12-DIFF: the authority join answered differently from the "
            "independently instantiated repaired instrument at "
            f"{result['stats']['joinVsRepairedMismatches']} enumerated position(s), "
            f"e.g. {result['firstMismatches'][:4]}")
    if result["stats"]["guardedEscapes"]:
        findings.append("EP12-DIFF: the join raised out of its total boundary at "
                        f"{result['stats']['guardedEscapes']} position(s)")
    if not result["discriminatingCardinality"]:
        findings.append("EP12-DIFF: the differential oracle has ZERO discriminating "
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


def injection_isolation_probe(intent, authority, snapshots):
    """RES-EP12-13, MEASURED rather than asserted.

    The predecessor's residual claimed a CONSEQUENCE of the shared-injection-table
    hazard that ep11.review-independent.json could not reproduce in five
    configurations and that a direct probe over 186 paths found no mechanism for.
    That review is right and there was nothing for the earlier review to catch.
    So this run measures the PREMISE instead of restating the consequence: it
    drives every mutable member of the injection table through the join, an
    independent repaired instance and the superseded instrument, and reports
    whether any of them mutated the table member it was handed.
    """
    baseline = {label: copy.deepcopy(value) for label, value in HOSTILE_VALUES
                if label in MUTABLE_HOSTILE_LABELS}
    table = dict(HOSTILE_VALUES)
    _census, paths = node_census(intent)
    scalar_paths = []
    for path in paths:
        if not path:
            continue
        try:
            current = _at(intent, path)
        except MALFORMED:
            continue
        if not isinstance(current, (dict, list)):
            scalar_paths.append(path)
    try:
        private = _private_module(snapshots, C2V4, "_ep12_isolation")
        c4 = json.loads(snapshots[C2V4_CONTRACT].decode("utf-8"),
                        object_pairs_hook=_pairs)
        relations = set(json.loads(snapshots[FACT_PLANE].decode("utf-8"),
                                   object_pairs_hook=_pairs)
                        ["relationRegistry"]["relations"])
    except (AuthorityLoadError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError, *MALFORMED) as exc:
        return {"error": f"{type(exc).__name__}: {exc}", "guardsDriven": 0,
                "casesDriven": 0, "sharedValuesMutated": ["UNMEASURED"],
                "injectorDeepCopies": False}
    v3 = authority.module(C2V3)
    c3 = authority.json(C2V3_CONTRACT)
    cases = 0
    for label in MUTABLE_HOSTILE_LABELS:
        injected = table[label]
        for path in scalar_paths:
            mutated = _inject(intent, path, injected)
            cases += 1
            for module, contract in ((private, c4), (v3, c3)):
                try:
                    module.validate_plan_intent(mutated, contract, relations)
                except MALFORMED:
                    continue
            try:
                c2_validate_intent(mutated, authority)
            except Exception:  # noqa: BLE001
                continue
    moved = sorted(label for label in MUTABLE_HOSTILE_LABELS
                   if not strict_equal(table[label], baseline[label]))
    # The structural half, measured on this run's own injector: the value written
    # into the mutated document must not BE the table member.
    probe = _inject(intent, scalar_paths[0], table["json-object-leaf"]) \
        if scalar_paths else None
    deep_copied = probe is not None and \
        _at(probe, scalar_paths[0]) is not table["json-object-leaf"]
    return {"guardsDriven": 3, "casesDriven": cases,
            "mutableTableMembers": list(MUTABLE_HOSTILE_LABELS),
            "sharedValuesMutated": moved, "injectorDeepCopies": deep_copied}


# --------------------------------------------------------------------------
# Section 6.  Source tripwires.  DECLARED SCOPE, so nothing here is over-read.
#
# ONE RULE GOVERNS THIS WHOLE SECTION, and it is the repair of IR-EP11-02: NO
# PROPERTY THIS INSTRUMENT PUBLISHES RESTS ON A SPELLING ENUMERATION.  The
# introspection tripwire is therefore NOT a scored guard: it is excluded from
# GUARD_IDS, it catches nothing in the evasion matrix by construction, and the
# class it used to be the sole catcher of is published as a DECLARED, MEASURED
# ESCAPE instead.  Its own blindness is measured on every run rather than
# conceded in prose: variant RX2c is spelled with six identifiers the enumeration
# does not name and this run publishes the scan's verdict on it.
# --------------------------------------------------------------------------

_SCAN_CACHE: dict[str, Any] = {}


def _own_source() -> bytes:
    if "source" not in _SCAN_CACHE:
        # RES-EP12-05: the instrument's own bytes are by construction not in its
        # own pinned set.  Recorded so the trust-order claim is not over-read.
        _SCAN_CACHE["source"] = (HERE / pathlib.Path(__file__).name).read_bytes()
    return _SCAN_CACHE["source"]


def _own_tree():
    if "tree" not in _SCAN_CACHE:
        _SCAN_CACHE["tree"] = ast.parse(_own_source())
    return _SCAN_CACHE["tree"]


def own_source_is_pinned() -> bool:
    """MEASURED, not asserted: this file is not a member of its own pin table."""
    return pathlib.Path(__file__).name in ALL_PINS


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


# Primitives by which code inside the route region could reach this guard's
# private state.  This is an ENUMERATION and it is NOT a proof; it is a tripwire
# that makes the cheap spellings visible.  It is deliberately left at the
# predecessor's list plus this instrument's own private names, so that RX2c —
# built from the six spellings ep11.review-independent.json used to defeat it —
# still escapes it and the escape is MEASURED and PUBLISHED on every run rather
# than closed by adding six more strings and claiming the class.
INTROSPECTION_NAMES = frozenset((
    "_getframe", "f_locals", "f_globals", "f_back", "f_code", "__closure__",
    "cell_contents", "__code__", "__globals__", "__traceback__", "tb_frame",
    "tb_next", "gi_frame", "cr_frame", "globals", "vars", "dir", "gc",
    "get_referrers", "get_objects", "getattr", "setattr", "delattr",
    "__getattribute__", "__getattr__", "__class__", "__dict__", "__mro__",
    "__subclasses__", "__base__", "__bases__", "__builtins__", "__import__",
    "exec", "eval", "compile", "importlib", "sys", "exc_info", "produced",
    "records", "anchors", "witness", "_Witness", "_WitnessRecord", "_anchored",
    "_anchored_server", "_private_module", "installation"))


def route_region_text(source_text: str | None = None) -> str:
    text = _own_source().decode("utf-8") if source_text is None else source_text
    begin, end = _route_region(text)
    return text[begin:end]


def route_introspection_scan(source_text=None):
    """Tripwire: the route region reads its arguments; it does not read the guard.

    Scans the WHOLE region between the markers — every function, helper, class
    body and expression the mutation is permitted to write.  It visits ast.alias
    as well as ast.Name and ast.Attribute, which the predecessor's walk did not,
    so `import sys as s` is no longer invisible to it.

    DECLARED BLIND SPOT, and it is the important one: this is an ENUMERATION of
    spellings.  A spelling it does not name reaches the guard's private state
    undetected.  Three tamper variants are built and executed on every ordinary
    run — AX6 plain, AX9 obfuscated, RX2c spelled with the six identifiers this
    list omits — and this run publishes the scan's verdict on each.  Because no
    published property depends on this scan, its blindness costs nothing that is
    not already declared in RES-EP12-02.
    """
    region = route_region_text(source_text)
    try:
        tree = ast.parse(region)
    except SyntaxError as exc:  # pragma: no cover - authoring error
        return {"regionCharacters": len(region),
                "introspectionSites": [f"region does not parse: {exc}"]}
    offenders = []
    for node in ast.walk(tree):
        identifiers = []
        if isinstance(node, ast.Attribute):
            identifiers.append(node.attr)
        elif isinstance(node, ast.Name):
            identifiers.append(node.id)
        elif isinstance(node, ast.alias):
            identifiers.append(node.name)
            if node.asname:
                identifiers.append(node.asname)
        for identifier in identifiers:
            if identifier in INTROSPECTION_NAMES:
                offenders.append(f"line {getattr(node, 'lineno', 0)}: {identifier}")
    declared = {node.name for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    missing = [name for name in C2_JOIN_CLOSURE if name not in declared]
    for name in missing:
        offenders.append(f"the route region does not define {name}")
    return {"regionCharacters": len(region),
            "regionDefinitions": len(declared),
            "enumeratedSpellings": len(INTROSPECTION_NAMES),
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
    """Tripwire: a bare numeric comparison against a literal IS the LB-C2-01 bug.

    RES-EP12-15: this is exactly the class adjudicated BLOCKING in check-c2-v4.py
    itself today, at three sites in its own _census_findings, where an unpinned
    wire value is compared against a computed int with a bare `!=`.
    """
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
    a single byte of source.  It does NOT see a mutation of a module-level
    CONTAINER's contents, which is why this instrument's load-time installation
    capture is a local threaded by parameter and not a module-level table.
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
     "answer_provenance_guard: A-1..A-8 over every pinned vector, reading no "
     "source at all"),
    ("route-introspection",
     "the route region names no primitive by which it could read or rewrite the "
     "guard's private state; an ENUMERATION, supporting NO published property",
     "answer_provenance_guard A-6 and A-8: the load-time installation, the anchor "
     "objects, their code objects and the anchored instance's own bindings, all "
     "re-checked by object identity across the drive"),
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
# parent's verified authority.  OBJECT variants attack the Authority and the
# ledger rather than the source.  Every layer is scored SEPARATELY and the
# unflattering cells are published.
#
# NEW IN v12, and the reason this section exists in this form:
#
#   RX1  ep11.review-independent.json's BLOCKING evasion, rebuilt by this
#        candidate's author before v12 was designed and MEASURED against v11's
#        own bytes in Section 8: on its first call it installs its own serving
#        function on authority.c2v4()'s attribute, wrapped by the ledger's OWN
#        _wrap under the repaired tag.  It uses no frame, no sys, no
#        getattr/setattr and no dunder of any kind.  Under v11 it exits 0 with
#        the complete green banner while 7 of 7 pinned verdicts come out of
#        check-c2.py.
#   RX3  the same class spelled as a WRAPPER around whatever is at the seat,
#        including this guard's own anchored server.
#   RX4  a genuine, anchor-produced object REPLAYED from an earlier window.  The
#        corpus carries ONE distinct PlanIntent across all seven vectors, so its
#        argument fingerprint matches every vector; the predecessor's witness
#        accumulated across vectors and would have accepted it.
#   RX6  the same seat substitution spelled through a DIFFERENT declared
#        accessor, authority.module(...) rather than authority.c2v4().
#   RX5  (object) the repaired module's three seats rebound to ledger-wrapped
#        servers backed by the SUPERSEDED originals under the repaired tag,
#        BEFORE the run captures anything.  A-6 cannot see this one — there is
#        nothing for it to compare against — and A-2 catches it anyway, which is
#        the whole point of anchoring on bytes rather than on a seat.
#   RX2c a witness forgery spelled with six identifiers INTROSPECTION_NAMES does
#        not enumerate.  It is expected to escape both the tripwire and every
#        scored guard, and both are MEASURED.
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
    """AX2, the blocking evasion of ep10.review-independent.json, rebuilt.

    A real, correctly-argumented, LEDGER-RECORDED call into the repaired module
    is made for every input.  Its result is returned only for the probe family —
    exactly the set of positions at which the two instruments diverge, so the
    differential oracle sees agreement everywhere.  For every REAL pinned vector
    the result is DISCARDED and the superseded module's answer is returned
    through the ledger's own unwrapped original, which records nothing.
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
    canonical preimage, so no superseded call is recorded at any depth.
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
    """AX8: the strongest answer substitution that touches neither seat nor frame.

    It defeats A-3 and A-4 by DETECTING the sentinel differentially: it calls
    both instruments and, whenever they disagree — which on a pinned vector means
    one of them has been poisoned — returns the repaired module's answer, so both
    sentinel-flow rules hold.  When they agree it returns the superseded module's
    object and forges a ledger entry and a provenance record for it, so the
    shared ledger says the repaired module produced it.
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
    """A forged ledger entry replayed for an unwrapped superseded call."""
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
    """AX6: AX8 plus a stack walk that overwrites the guard's PRIVATE record.

    This is RES-EP12-02's declared boundary, BUILT AND EXECUTED.  It does not
    forge a new record — record parity would see that — it reaches the record the
    guard's own anchored server appended and replaces the object it names.  Every
    behavioural rule the answer-provenance guard has then holds.  It is spelled
    plainly, so the tripwire sees it; RX2c is the same attack spelled so the
    tripwire does not.
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
        seen = None
        while frame is not None and seen is None:
            seen = frame.f_locals.get("witness")
            frame = frame.f_back
        if seen is not None:
            for item in reversed(seen.records):
                if item.api == "validate_plan_intent" and item.depth == 0:
                    item.result = answer
                    break
        return answer
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_OBFUSCATED_TAMPER = '''
def _reach(subject, parts):
    return getattr(subject, "".join(parts))


def c2_validate_intent(intent, authority):
    """AX9: the same tamper as AX6, spelled so that every attribute name is
    assembled at run time and the frame is taken from an exception rather than
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
            for item in reversed(_reach(seen, ("reco", "rds"))):
                if item.api == "validate_plan_intent" and item.depth == 0:
                    item.result = answer
                    break
        return answer
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_UNENUMERATED_TAMPER = '''
import inspect as _probe
import operator as _op

_UP = _op.attrgetter("f_b" + "ack")
_SEE = _op.attrgetter("f_loc" + "als")
_REC = _op.attrgetter("reco" + "rds")


def c2_validate_intent(intent, authority):
    """RX2c: AX6's tamper spelled with SIX identifiers INTROSPECTION_NAMES does
    not enumerate — inspect, operator, _probe, _op, attrgetter, currentframe —
    plus attribute names assembled from string constants, which the scan never
    inspects.  Nothing here is more exotic than two stdlib modules.  Its purpose
    is to be MEASURED escaping the tripwire, so that no property this instrument
    publishes can rest on the enumeration."""
    try:
        relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
        ledger = authority.ledger
        repaired = authority.c2v4().validate_plan_intent(
            intent, authority.json(C2V4_CONTRACT), relations)
        hidden = ledger.originals[(C2V3, "validate_plan_intent")]
        answer = hidden(intent, authority.json(C2V3_CONTRACT), relations)
        if repaired != answer:
            return repaired
        here = _probe.currentframe()
        seen = None
        while here is not None and seen is None:
            seen = _SEE(here).get("witness")
            here = _UP(here)
        if seen is not None:
            for item in reversed(_REC(seen)):
                if item.api == "validate_plan_intent" and item.depth == 0:
                    item.result = answer
                    break
        return answer
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_RX1_SEAT = '''
_ARMED = []


def c2_validate_intent(intent, authority):
    """RX1: ep11.review-independent.json IR-EP11-01, rebuilt.

    On its FIRST call it installs its own serving function AT THE SEAT the
    predecessor's witness tagged from, wrapped by the ledger's OWN _wrap under
    the repaired tag.  It uses no frame, no sys, no getattr/setattr and no dunder
    of any kind: everything it touches is reached by ordinary attribute access on
    the two objects the route region is handed by design.
    """
    try:
        contract = authority.json(C2V4_CONTRACT)
        relations = authority.json(FACT_PLANE)["relationRegistry"]["relations"]
        if not _ARMED:
            _ARMED.append(1)
            ledger = authority.ledger
            v4 = ledger.originals[(C2V4, "validate_plan_intent")]
            v3 = ledger.originals[(C2V3, "validate_plan_intent")]
            c4 = authority.json(C2V4_CONTRACT)
            c3 = authority.json(C2V3_CONTRACT)

            def serve(value, _contract, _relations):
                if _is_probe_family(value):
                    return v4(value, c4, _relations)
                return v3(value, c3, _relations)

            authority.c2v4().validate_plan_intent = ledger._wrap(
                serve, "validate_plan_intent", C2V4)
        return authority.c2v4().validate_plan_intent(
            intent, contract, set(relations))
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_RX3_WRAP = '''
_WRAPPED = []


def c2_validate_intent(intent, authority):
    """RX3: wrap whatever is at the seat — including this guard's own anchored
    server — and substitute the answer, then put the wrapper back at the seat
    through the declared accessor."""
    try:
        contract = authority.json(C2V4_CONTRACT)
        relations = authority.json(FACT_PLANE)["relationRegistry"]["relations"]
        ledger = authority.ledger
        seat = authority.c2v4().validate_plan_intent
        if not _WRAPPED or seat is not _WRAPPED[0]:
            inner = seat
            c3 = authority.json(C2V3_CONTRACT)
            hidden = ledger.originals[(C2V3, "validate_plan_intent")]

            def wrapper(value, _contract, _relations):
                honest = inner(value, _contract, _relations)
                other = hidden(value, c3, _relations)
                if honest != other:
                    return honest
                return other

            del _WRAPPED[:]
            _WRAPPED.append(wrapper)
            authority.c2v4().validate_plan_intent = wrapper
        return authority.c2v4().validate_plan_intent(
            intent, contract, set(relations))
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_RX4_REPLAY = '''
_STALE = []


def c2_validate_intent(intent, authority):
    """RX4: return a GENUINE object the repaired instrument produced — for an
    EARLIER window.  The corpus carries one distinct PlanIntent across all seven
    vectors, so the argument fingerprint matches every one of them and a witness
    that accumulates across vectors accepts a replayed object."""
    try:
        contract = authority.json(C2V4_CONTRACT)
        relations = authority.json(FACT_PLANE)["relationRegistry"]["relations"]
        answer = authority.c2v4().validate_plan_intent(
            intent, contract, set(relations))
        if answer or _is_probe_family(intent):
            return answer
        if _STALE:
            return _STALE[0]
        _STALE.append(answer)
        return answer
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", "boundary")]
'''

_RX6_MODULE_SEAT = '''
_ARMED6 = []


def c2_validate_intent(intent, authority):
    """RX6: the same seat substitution as RX1, spelled through a DIFFERENT
    declared accessor — authority.module(...) rather than authority.c2v4()."""
    try:
        contract = authority.json(C2V4_CONTRACT)
        relations = authority.json(FACT_PLANE)["relationRegistry"]["relations"]
        if not _ARMED6:
            _ARMED6.append(1)
            ledger = authority.ledger
            v4 = ledger.originals[(C2V4, "validate_plan_intent")]
            v3 = ledger.originals[(C2V3, "validate_plan_intent")]
            c4 = authority.json(C2V4_CONTRACT)
            c3 = authority.json(C2V3_CONTRACT)

            def serve(value, _contract, _relations):
                if _is_probe_family(value):
                    return v4(value, c4, _relations)
                return v3(value, c3, _relations)

            authority.module(C2V4).validate_plan_intent = ledger._wrap(
                serve, "validate_plan_intent", C2V4)
        return authority.c2v4().validate_plan_intent(
            intent, contract, set(relations))
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
         "a real, correctly-argumented, ledger-recorded call into the repaired "
         "module whose result is DISCARDED for every real pinned vector, "
         "returning the superseded module's answer; commit and canonical honest "
         "and the probe family whitelisted so the oracle sees agreement",
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
         "RES-EP12-02's declared boundary, BUILT AND EXECUTED: AX8 plus a "
         "sys._getframe stack walk that overwrites the object named by the "
         "guard's own anchored record",
         _FRAME_TAMPER + _HONEST_COMMIT_AND_CANONICAL),
        ("AX9-obfuscated-witness-forgery",
         "the same tamper as AX6 with every enumerated identifier assembled at "
         "run time and the frame taken from an exception rather than from sys",
         _OBFUSCATED_TAMPER + _HONEST_COMMIT_AND_CANONICAL),
        ("RX2c-unenumerated-witness-forgery",
         "the same tamper spelled with six identifiers the introspection "
         "enumeration does not name — inspect, operator, _probe, _op, attrgetter, "
         "currentframe — and attribute names assembled from string constants the "
         "scan never inspects; built to MEASURE that the tripwire is blind to it",
         _UNENUMERATED_TAMPER + _HONEST_COMMIT_AND_CANONICAL),
        ("RX1-seat-substitution-declared-accessor",
         "ep11.review-independent.json IR-EP11-01: its own serving function "
         "installed on authority.c2v4()'s attribute, wrapped by the ledger's OWN "
         "_wrap under the repaired tag, with no introspection of any kind",
         _PROBE_HELPER + _RX1_SEAT + _HONEST_COMMIT_AND_CANONICAL),
        ("RX3-seat-wrapping-of-the-guards-own-server",
         "wraps whatever is at the seat — including this guard's anchored server "
         "inside the measured window — and puts the wrapper back through the "
         "declared accessor",
         _RX3_WRAP + _HONEST_COMMIT_AND_CANONICAL),
        ("RX4-stale-anchored-object-replay",
         "returns a GENUINE object the repaired instrument produced, replayed "
         "from an earlier window; one distinct PlanIntent means its argument "
         "fingerprint matches every vector",
         _PROBE_HELPER + _RX4_REPLAY + _HONEST_COMMIT_AND_CANONICAL),
        ("RX6-seat-substitution-module-accessor",
         "the same seat substitution as RX1 spelled through a DIFFERENT declared "
         "accessor, authority.module(...) rather than authority.c2v4()",
         _PROBE_HELPER + _RX6_MODULE_SEAT + _HONEST_COMMIT_AND_CANONICAL),
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
        f"_ep12_evasion_{re.sub(r'[^0-9a-zA-Z]', '_', name)}")
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
        shadow = types.ModuleType("_ep12_unwrapped_c2v4")
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
    """Tag forgery at INSTALL time: the SUPERSEDED module is installed under the
    repaired tag and the repaired module under the superseded tag."""

    def __init__(self, inner, snapshots):
        super().__init__(inner)
        delegate = inner.delegate
        self.ledger = delegate.ServedLedger()
        self._v4 = _exec_verified(C2V4, snapshots[C2V4], prefix="_ep12_forge4")
        self._v3 = _exec_verified(C2V3, snapshots[C2V3], prefix="_ep12_forge3")
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
        real3 = _exec_verified(C2V3, snapshots[C2V3], prefix="_ep12_shim3")
        shim = types.ModuleType("_ep12_shim_c2v4")
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
        self._v4 = _exec_verified(C2V4, snapshots[C2V4], prefix="_ep12_rec4")
        self._v3 = _exec_verified(C2V3, snapshots[C2V3], prefix="_ep12_rec3")
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


def _contract_swapped(function, contract):
    def served(value, _contract, *rest):
        return function(value, contract, *rest)
    return served


class _SeatRebindAuthority(_AuthorityView):
    """RX5: the repaired module object is genuine, the ledger is genuine, every
    tag is genuine — and the three SEATS on that module have been rebound, before
    anything captured them, to ledger-wrapped servers backed by the SUPERSEDED
    originals under the repaired tag.

    This is IR-EP11-01's class with no source signature at all.  The load-time
    installation check A-6 cannot see it, because by the time anything looks the
    forgery IS the installation and it carries the ledger's own markers.  A-2
    catches it because A-2 does not ask what is at the seat: it asks whether the
    object returned came out of the function the verified bytes defined.
    """

    def __init__(self, inner, snapshots):
        super().__init__(inner)
        delegate = inner.delegate
        self.ledger = delegate.ServedLedger()
        self._v4 = _exec_verified(C2V4, snapshots[C2V4], prefix="_ep12_seat4")
        self._v3 = _exec_verified(C2V3, snapshots[C2V3], prefix="_ep12_seat3")
        self.ledger.install(self._v4, C2V4)
        self.ledger.install(self._v3, C2V3)
        contract3 = inner.json(C2V3_CONTRACT)
        for api in C2_IMPORTED_APIS:
            hidden = self.ledger.originals[(C2V3, api)]
            served = _contract_swapped(hidden, contract3)
            self.ledger.originals[(C2V4, api)] = served
            setattr(self._v4, api, self.ledger._wrap(served, api, C2V4))
        self.modules = {C2V4: self._v4, C2V3: self._v3}

    def module(self, name):
        return self.modules[name]

    def c2v4(self):
        return self._v4

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
        ("RX5-seat-rebind-before-capture",
         "the genuine repaired module's three seats rebound to ledger-wrapped "
         "superseded-backed servers under the repaired tag, before anything "
         "captured the installation; A-6 cannot see it and A-2 does",
         lambda inner: _SeatRebindAuthority(inner, snapshots)),
    )


# The SCORED guard set.  The introspection tripwire is deliberately NOT a member:
# IR-EP11-02 found it blocking that an enumeration of spellings was the sole
# guard for a class, and the repair is to stop counting it as a guard rather than
# to lengthen the enumeration.  Its verdict on every variant is still measured
# and published, in tripwireOutcome, where it supports nothing.
GUARD_IDS = ("answerProvenance", "callProvenance", "differentialOracle",
             "supersededCrossCheck", "c2RouteScan")

SOURCE_READING_GUARDS = ("c2RouteScan",)


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
    """Run every scored guard against one hostile configuration.

    The installation is captured BEFORE the variant's route region has run and
    restored AFTER it has been scored, so a variant whose write persists cannot
    move the next variant's numbers.  The guards run in the PRODUCTION ordering —
    call provenance, then answer provenance — so no result here depends on an
    ordering the shipped run does not use.
    """
    fired = {}
    installation = capture_installation(hostile)
    try:
        try:
            call_findings, _measure = module.call_provenance_guard(named, hostile)
        except Exception as exc:  # noqa: BLE001
            call_findings = [f"EP12-CALL: raised {type(exc).__name__}: {exc}"]
        fired["callProvenance"] = bool(call_findings)
        try:
            answer_findings, _counts, _rows = module.answer_provenance_guard(
                named, hostile, snapshots, installation)
        except Exception as exc:  # noqa: BLE001
            answer_findings = [f"EP12-ANSWER: raised {type(exc).__name__}: {exc}"]
        fired["answerProvenance"] = bool(answer_findings)
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
            tripwire = None
        else:
            scan = c2_route_scan(tree)
            fired["c2RouteScan"] = bool(
                scan["unroutedSitesInsideJoin"]
                or scan["referencesOutsideDeclaredClosure"]
                or scan["authorityRoutedSites"] < len(C2_IMPORTED_APIS))
            tripwire = bool(
                route_introspection_scan(mutated_text)["introspectionSites"])
    finally:
        restore_installation(installation, hostile)
    return fired, tripwire


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
        fired, tripwire = _score(module, named_intents, authority, oracle_intent,
                                 snapshots, delegate, tree, mutated)
        rows.append({"variant": name, "why": why, "class": "source", "built": True,
                     "tripwire": tripwire,
                     **{key: fired[key] for key in GUARD_IDS}})

    for name, why, factory in object_attacks(snapshots):
        try:
            hostile = factory(authority)
        except Exception as exc:  # noqa: BLE001
            rows.append({"variant": name, "why": why, "class": "object",
                         "built": False, "error": f"{type(exc).__name__}: {exc}"})
            continue
        fired, tripwire = _score(_current_module(), named_intents, hostile,
                                 oracle_intent, snapshots, delegate, None)
        rows.append({"variant": name, "why": why, "class": "object", "built": True,
                     "tripwire": tripwire,
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
    tripwire_rows = [{"variant": row["variant"], "flagged": row.get("tripwire")}
                     for row in built if row["class"] == "source"]
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
        "tripwireOutcome": tripwire_rows,
    }


# --------------------------------------------------------------------------
# Section 8.  Preserved measurement by delegation, positive controls, and the
# PREDECESSOR-DEFEAT CONTROL.
#
# The last of these is what makes "repaired" a measurement rather than a claim.
# It rebuilds ep11.review-independent.json's blocking evasion RX1 inside
# check-evaluation-proof-v11.py's OWN route region, from v11's SHA-256-verified
# bytes, drives it in the production ordering v11's heavy_measurements uses, and
# requires:
#   * v11's answer_provenance_guard to return ZERO findings with every rule at
#     full agreement — that is the defect, reproduced in the predecessor;
#   * the validation verdict for 7 of 7 pinned vectors to be produced by
#     check-c2.py under that variant, and by check-c2-v4.py for the UNMODIFIED
#     predecessor in the identical harness — that is the consequence, measured;
#   * this instrument's own guard to produce findings for the same variant —
#     that is the repair, measured.
# If any of the three stops holding, this run reports it.  Nothing here is
# transcribed from the review.
# --------------------------------------------------------------------------

def preserved_measurements(authority, snapshots):
    """Execute the reviewer-verified v10 measurement from its verified bytes."""
    delegate = authority.delegate
    heavy = delegate.heavy_measurements(authority.inner)
    v10_candidate = authority.json(EP10_ARTIFACT)
    # Driven at the DELEGATE's own top level, not nested: v10's behavioural
    # counterparts only run when its nesting depth is zero, and a run that
    # skipped them would report findings about counterparts that were never
    # executed rather than about the measurements this candidate preserves.
    try:
        v10_findings = delegate.check(copy.deepcopy(v10_candidate), authority.inner)
    except Exception as exc:  # noqa: BLE001
        v10_findings = [f"the delegate's own checking layer raised "
                        f"{type(exc).__name__}: {exc}"]
    return heavy, v10_findings


class _Sandbox:
    """An authority-shaped object over FRESH instances and a FRESH ledger.

    Controls are driven here rather than against the run's own authority so that
    a control which rebinds a seat cannot move the numbers the run publishes.
    """

    def __init__(self, authority, snapshots, prefix):
        delegate = authority.delegate
        self.delegate = delegate
        self.ledger = delegate.ServedLedger()
        self._modules = {
            C2V4: _exec_verified(C2V4, snapshots[C2V4], prefix=prefix + "4"),
            C2V3: _exec_verified(C2V3, snapshots[C2V3], prefix=prefix + "3"),
        }
        self.ledger.install(self._modules[C2V4], C2V4)
        self.ledger.install(self._modules[C2V3], C2V3)
        self.modules = self._modules
        self._authority = authority
        self._snapshots = snapshots
        self.cache: dict[str, Any] = {}
        self.measurement: dict[str, Any] = {}

    def json(self, name):
        return self._authority.json(name)

    def module(self, name):
        return self._modules.get(name)

    def c2v4(self):
        return self._modules[C2V4]

    def c2v3(self):
        return self._modules[C2V3]


def _mutated_region(source_text: str, region: str) -> str:
    begin, end = _route_region(source_text)
    return source_text[:begin] + region + source_text[end:]


def _exec_named(name: str, filename: str, source_text: str):
    module = types.ModuleType(f"_ep12_{re.sub(r'[^0-9a-zA-Z]', '_', name)}")
    module.__dict__["__file__"] = str(HERE / filename)
    exec(compile(source_text, f"<{name}>", "exec"), module.__dict__)  # noqa: S102
    return module


def _seat_attribution(module, sandbox, named_intents):
    """Which module's BYTES produced each validation verdict, measured by seat.

    Every reachable spelling of validate_plan_intent on both module objects is
    wrapped in a marker that calls through and records the produced object
    against the seat it came out of; the marker retains the object so no id can
    be recycled, and the INNERMOST marker wins.  This reads nothing the checker
    publishes: it is an independent attribution of the answer.
    """
    api = "validate_plan_intent"
    seats: dict[int, str] = {}
    retained: list[Any] = []

    def marker(inner, seat):
        def marked(*args, **kwargs):
            result = inner(*args, **kwargs)
            retained.append(result)
            seats.setdefault(id(result), seat)
            return result
        return marked

    ledger = sandbox.ledger
    for tag in (C2V4, C2V3):
        target = sandbox.module(tag)
        setattr(target, api, marker(getattr(target, api), tag))
        if (tag, api) in ledger.originals:
            ledger.originals[(tag, api)] = marker(ledger.originals[(tag, api)], tag)

    # PRODUCTION ORDERING: the call-provenance drive happens first, in plain
    # ledger windows that neither save nor restore the module attributes.
    try:
        module.call_provenance_guard(named_intents, sandbox)
    except Exception:  # noqa: BLE001
        pass
    tally: dict[str, int] = {}
    for vector_id, intent in named_intents:
        try:
            with ledger.window(f"attribution:{vector_id}"):
                answer = module.c2_join(intent, sandbox)
            seat = seats.get(id(answer["verdict"]), "UNATTRIBUTED")
        except Exception:  # noqa: BLE001
            seat = "RAISED"
        tally[seat] = tally.get(seat, 0) + 1
    return tally


def predecessor_defeat_control(named_intents, authority, snapshots):
    """MEASURED: the blocking evasion defeats v11 and is caught here."""
    variant = "RX1-seat-substitution-declared-accessor"
    region = _PROBE_HELPER + _RX1_SEAT + _HONEST_COMMIT_AND_CANONICAL
    result: dict[str, Any] = {
        "predecessor": EP11,
        "predecessorSha256": ALL_PINS[EP11],
        "variant": variant,
        "method": PREDECESSOR_CONTROL_METHOD,
    }
    try:
        predecessor_text = snapshots[EP11].decode("utf-8")
        mutated_text = _mutated_region(predecessor_text, region)
        forged = _exec_named("predecessor_rx1", EP11, mutated_text)
        honest = _exec_named("predecessor_honest", EP11, predecessor_text)
        for module in (forged, honest):
            # Trust order: neither predecessor instance re-opens its own path.
            module._SCAN_CACHE["source"] = snapshots[EP11]
            module._SCAN_CACHE["tree"] = ast.parse(snapshots[EP11])
        result["predecessorSourceCacheSeeded"] = (
            forged._SCAN_CACHE.get("source") == snapshots[EP11]
            and honest._SCAN_CACHE.get("source") == snapshots[EP11])
        result["mutationScope"] = _region_scope(predecessor_text, mutated_text)

        authority.cache["predecessorModule"] = honest
        sandbox = _Sandbox(authority, snapshots, "_ep12_pred_guard")
        forged.call_provenance_guard(named_intents, sandbox)
        findings, counts, _rows = forged.answer_provenance_guard(
            named_intents, sandbox, snapshots)
        result["predecessorAnswerProvenanceFindings"] = len(findings)
        result["predecessorExpectedPerRuleTotal"] = counts["expectedPerRuleTotal"]
        result["predecessorObjectProvenanceAgreements"] = counts[
            "objectProvenanceAgreements"]
        result["predecessorAllRulesHeld"] = bool(counts["allRulesHeld"])
        result["predecessorIsDefeated"] = (
            not findings and bool(counts["allRulesHeld"]))

        # FRESH instances: a route region that arms once holds its armed flag
        # in a module global, so an instance already driven above would not arm
        # again and the attribution would measure the wrong thing.
        forged_tally = _seat_attribution(
            _exec_named("predecessor_rx1_attribution", EP11, mutated_text),
            _Sandbox(authority, snapshots, "_ep12_pred_forged"), named_intents)
        honest_tally = _seat_attribution(
            _exec_named("predecessor_honest_attribution", EP11, predecessor_text),
            _Sandbox(authority, snapshots, "_ep12_pred_honest"), named_intents)
        result["verdictsUnderTheVariantBy"] = dict(sorted(forged_tally.items()))
        result["verdictsUnderTheUnmodifiedPredecessorBy"] = dict(
            sorted(honest_tally.items()))
        result["variantRoutesEveryPinnedVerdictToTheSupersededEncoder"] = (
            forged_tally.get(C2V3) == len(named_intents))
        result["unmodifiedPredecessorRoutesEveryPinnedVerdictToTheRepairedModule"] \
            = honest_tally.get(C2V4) == len(named_intents)

        own_text = _mutated_region(_own_source().decode("utf-8"), region)
        own = _exec_variant("predecessor-control-" + variant, own_text)
        own_sandbox = _Sandbox(authority, snapshots, "_ep12_own_guard")
        installation = capture_installation(own_sandbox)
        own.call_provenance_guard(named_intents, own_sandbox)
        own_findings, own_counts, _rows = own.answer_provenance_guard(
            named_intents, own_sandbox, snapshots, installation)
        result["thisInstrumentAnswerProvenanceFindings"] = len(own_findings)
        result["thisInstrumentInstallationIntact"] = own_counts[
            "installationIntact"]
        result["thisInstrumentAnchoredObjectAgreements"] = own_counts[
            "anchoredObjectAgreements"]
        result["thisInstrumentCatchesIt"] = bool(own_findings)
        result["thisInstrumentVerdictsBy"] = dict(sorted(_seat_attribution(
            _exec_variant("predecessor-control-attribution-" + variant, own_text),
            _Sandbox(authority, snapshots, "_ep12_own_attribution"),
            named_intents).items()))
        result["thisInstrumentDetectsRatherThanPrevents"] = (
            result["thisInstrumentVerdictsBy"].get(C2V3) == len(named_intents)
            and bool(own_findings))
        result["firstFindingHere"] = own_findings[0][:200] if own_findings else None
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["predecessorIsDefeated"] = False
        result["thisInstrumentCatchesIt"] = False
    return result


PREDECESSOR_CONTROL_METHOD = (
    "the blocking evasion of ep11.review-independent.json is rebuilt inside "
    "check-evaluation-proof-v11.py's OWN route region, from v11's SHA-256-verified "
    "bytes, with the text before # ROUTE-REGION-BEGIN and after # ROUTE-REGION-END "
    "byte-identical; both instruments are driven in the production ordering their "
    "own heavy_measurements uses (call provenance first, then answer provenance); "
    "and the module whose bytes produced each pinned verdict is attributed "
    "independently by seat markers that read nothing either instrument publishes.")


def _region_scope(base_text: str, mutated_text: str) -> str:
    begin, end = _route_region(base_text)
    tail = mutated_text.index(ROUTE_END)
    identical = (mutated_text[:begin] == base_text[:begin]
                 and mutated_text[tail:] == base_text[end:])
    return ("ONLY the route region; prefix and suffix byte-identical (asserted "
            f"on this run: {identical})")


def distinct_answer_probe(named_intents, authority, snapshots):
    """POSITIVE CONTROL on the guard: it must FAIL when the answer is not the
    repaired instrument's.

    A guard that has stopped discriminating passes everything, including an
    honest join, and no green banner can tell the difference.  Three deliberately
    substituted joins are driven through the SAME guard here, on FRESH sandboxes,
    and each is required to produce findings.  The forged-ledger row also shows,
    in numbers, why the shared served-module ledger cannot be what A-2 tests.
    """
    source_text = _own_source().decode("utf-8")
    rows = {}
    for label, region in (
            ("decoyCall", _PROBE_HELPER + _AX2_VALIDATE
             + _HONEST_COMMIT_AND_CANONICAL),
            ("forgedLedgerEntry", _REPLAY_VALIDATE
             + _HONEST_COMMIT_AND_CANONICAL),
            ("seatSubstitution", _PROBE_HELPER + _RX1_SEAT
             + _HONEST_COMMIT_AND_CANONICAL)):
        module = _exec_variant(f"positive-control-{label}",
                               _mutated_region(source_text, region))
        sandbox = _Sandbox(authority, snapshots, f"_ep12_control_{label}")
        installation = capture_installation(sandbox)
        module.call_provenance_guard(named_intents, sandbox)
        findings, counts, _rows = module.answer_provenance_guard(
            named_intents, sandbox, snapshots, installation)
        rows[label] = {
            "producesFindings": bool(findings),
            "findingCount": len(findings),
            "independentValueAgreements": counts["independentValueAgreements"],
            "anchoredObjectAgreements": counts["anchoredObjectAgreements"],
            "sharedLedgerAgreements": counts["sharedLedgerAgreements"],
            "repairedSentinelFlowed": counts["repairedSentinelFlowed"],
            "supersededSentinelIgnored": counts["supersededSentinelIgnored"],
            "installationIntact": counts["installationIntact"],
        }
    rows["allProduceFindings"] = all(
        rows[label]["producesFindings"]
        for label in ("decoyCall", "forgedLedgerEntry", "seatSubstitution"))
    return rows


# --------------------------------------------------------------------------
# Section 9.  Heavy measurement, computed once per verified authority.
# --------------------------------------------------------------------------

def heavy_measurements(authority, snapshots) -> dict[str, Any]:
    if "ep12" in authority.cache:
        return authority.cache["ep12"]
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
        heavy = {"named": [], "findings": ["EP12-VECTORS: no PlanIntent could be "
                                           "read from the pinned vector source"]}
        authority.cache["ep12"] = heavy
        return heavy

    # THE INSTALLATION IS CAPTURED HERE, before the first route-region call this
    # run makes, and threaded to the guards by PARAMETER.  It is not stored on
    # the Authority and not bound to a module global: the route region's globals
    # ARE this module's globals, so a module-level table would be writable from
    # inside the region by plain name and would anchor nothing.
    installation = capture_installation(authority)

    delegate_heavy, v10_findings = preserved_measurements(authority, snapshots)

    before = module_binding_fingerprint()
    call_findings, call_measure = call_provenance_guard(named, authority)
    answer_findings, answer_counts, answer_rows = answer_provenance_guard(
        named, authority, snapshots, installation)
    rebound = global_binding_probe(before)
    residual_installation_defects = installation_status(installation, authority)
    restore_installation(installation, authority)

    oracle = plan_intent_surface(named[0][1], authority, snapshots)
    oracle_findings = differential_oracle_findings(oracle)
    isolation = injection_isolation_probe(named[0][1], authority, snapshots)

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
    predecessor = predecessor_defeat_control(named, authority, snapshots)
    restore_installation(installation, authority)

    findings = list(call_findings) + list(answer_findings) + list(oracle_findings)
    findings += c2_api_surface(authority)
    if rebound:
        findings.append(f"EP12-BINDING: module-level binding(s) {rebound} changed "
                        "identity across the authority drive; a guard whose own "
                        "globals move underneath it is not measuring the join")
    if v10_findings:
        findings.append(
            "EP12-PRESERVED: the pinned predecessor candidate no longer passes its "
            f"own pinned checking layer on this run ({len(v10_findings)} "
            f"finding(s), first: {str(v10_findings[0])[:160]}); the measurements "
            "this candidate preserves by delegation are not reproduced")
    if not control["allProduceFindings"]:
        findings.append(
            "EP12-CONTROL: a join that demonstrably does not return the repaired "
            "instrument's answer produced NO answer-provenance finding; the guard "
            "has stopped discriminating and its green result means nothing")
    if isolation.get("error"):
        findings.append("EP12-ISOLATION: the injection-isolation probe could not "
                        f"run: {isolation['error']}")
    if isolation.get("sharedValuesMutated"):
        findings.append(
            "EP12-ISOLATION: a guard MUTATED the injection-table member it was "
            f"handed at {isolation['sharedValuesMutated']}; every surface count "
            "on this run is order-dependent and none of them is a measurement")
    if not isolation.get("injectorDeepCopies"):
        findings.append("EP12-ISOLATION: this run's injector did not deep-copy the "
                        "injected value into the mutated document")
    if predecessor.get("error"):
        findings.append("EP12-PREDECESSOR: the predecessor-defeat control could not "
                        f"run: {predecessor['error']}")
    if not predecessor.get("predecessorIsDefeated"):
        findings.append(
            "EP12-PREDECESSOR: the blocking evasion of ep11.review-independent.json "
            "did NOT come out silent against the predecessor's own guard on this "
            "run; the defect this candidate repairs is not reproduced, so the "
            "repair is unmeasured and must not be published as one")
    if not predecessor.get("thisInstrumentCatchesIt"):
        findings.append(
            "EP12-PREDECESSOR: this instrument's answer-provenance guard produced "
            "NO finding for the evasion that defeats the predecessor; IR-EP11-01 "
            "is unrepaired")

    heavy = {
        "named": named, "vectors": vectors, "findings": findings,
        "callProvenance": call_measure,
        "answerProvenance": answer_counts, "answerRows": answer_rows,
        "rebound": rebound,
        "installationDefectsAfterDrive": residual_installation_defects,
        "oracle": oracle, "descriptorSurface": descriptor_surface,
        "isolation": isolation,
        "evasion": evasion, "control": control, "predecessor": predecessor,
        "delegate": delegate_heavy, "v10Findings": v10_findings,
        "delegateSourceSealed": delegate_source_is_sealed(
            authority.delegate, snapshots),
    }
    authority.cache["ep12"] = heavy
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
        findings.append(f"EP12-TYPE: {label} must be the JSON integer type; got "
                        f"{type(value).__name__}")
        return False
    if expected is not None and value != expected:
        findings.append(f"EP12-TYPE: {label} must be {expected}; got {value}")
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
    for key in ("delegatedChecker", "predecessorInstrument", "executables",
                "pinnedData", "supersededIndependentEncoder"):
        entries = closure.get(key)
        if isinstance(entries, dict):
            entries = [entries]
        if not isinstance(entries, list):
            findings.append(f"EP12-RECORD: delegationClosure.{key} must be an array")
            continue
        for entry in entries:
            if not isinstance(entry, dict) or "file" not in entry or \
                    "sha256" not in entry:
                findings.append(f"EP12-RECORD: delegationClosure.{key} rows must "
                                "record file AND sha256; a count is not a record")
                continue
            declared[entry["file"]] = entry["sha256"]
    for name, expected in ALL_PINS.items():
        actual = sha_bytes(authority._snapshots[name])
        if actual != expected:  # pragma: no cover - load_snapshots refuses first
            findings.append(f"EP12-RECORD: {name} recomputes to {actual}, pinned at "
                            f"{expected}")
        if declared.get(name) != expected:
            findings.append(f"EP12-RECORD: the candidate records {name} as "
                            f"{declared.get(name)!r}; this run verified {expected}")
    for name in sorted(set(declared) - set(ALL_PINS)):
        findings.append(f"EP12-RECORD: the candidate records {name}, which this "
                        "checker does not pin or verify")

    checked = 0
    for holder, attribute in ((EP10, "ALL_PINS"), (EP11, "ALL_PINS"),
                              (EP8, "PINNED"), (EP7, "PINNED"), (EP6, "PINNED"),
                              (C2V4, "PINS")):
        if holder == EP10:
            module = authority.delegate
        elif holder == EP11:
            module = authority.cache.get("predecessorModule")
        else:
            module = authority.module(holder)
        table = getattr(module, attribute, None)
        if not isinstance(table, dict):
            continue
        checked += 1
        for name, sha in table.items():
            if name in ALL_PINS and ALL_PINS[name] != sha:
                findings.append(f"EP12-CLOSURE: {holder}.{attribute} pins {name} at "
                                f"{sha}; v12 verified {ALL_PINS[name]}")
    rule = closure.get("pinAgreementRule")
    if not isinstance(rule, str) or "of those that expose one" not in rule:
        findings.append("EP12-CLOSURE: pinAgreementRule must state that the "
                        "cross-check covers only the closure members that expose a "
                        "pin table ('of those that expose one'); several expose "
                        "none, and a total claim would quantify over a region the "
                        "instrument cannot observe")
    _expect(closure, "pinTablesCrossChecked", checked,
            "EP12-CLOSURE: delegationClosure", findings)
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


REQUIRED_RETRACTIONS = ("RET-EP12-01", "RET-EP12-02", "RET-EP12-03",
                        "RET-EP12-04")

RETRACTION_CONTENT = {
    "RET-EP12-01": ("the seat the route region owns", "not whose bytes computed it",
                    "RX1"),
    "RET-EP12-02": ("sole guard", "an enumeration of spellings is not a proof"),
    "RET-EP12-03": ("could not be reproduced", "structurally, not accidentally"),
    "RET-EP12-04": ("claimed completeness", "was not complete"),
}


def retraction_checks(contract, authority) -> list[str]:
    """IR-EP11-NB-02: the verbatim fragment must be substantive, must occur inside
    the NAMED SUBJECT, and the named subject must RESOLVE TO A STRING.

    The predecessor located its fragment at the granularity of a JSON OBJECT, so
    a fragment lifted verbatim from a different part of that object satisfied it
    while the retraction no longer quoted the sentence it retracted.  Requiring
    the subjectPath to resolve to a string narrows the location to the claim.
    """
    findings: list[str] = []
    retractions = contract.get("retractions")
    if not isinstance(retractions, list) or not retractions:
        return ["EP12-RETRACT: retractions must be a non-empty array"]
    by_id = {item.get("id"): item for item in retractions
             if isinstance(item, dict)}

    for retraction_id in REQUIRED_RETRACTIONS:
        entry = by_id.get(retraction_id)
        if not isinstance(entry, dict):
            findings.append(f"EP12-RETRACT: {retraction_id} is absent")
            continue
        if entry.get("disposition") != "RETRACTED-AS-FALSE":
            findings.append(f"EP12-RETRACT: {retraction_id} must be disposed "
                            "RETRACTED-AS-FALSE; a retraction may not be softened "
                            "into a scoping note")
        quoted = entry.get("retractedText")
        subject_file = entry.get("subjectFile")
        subject_path = entry.get("subjectPath")
        if not isinstance(quoted, str) or len(quoted) < RETRACTION_MIN_FRAGMENT:
            findings.append(
                f"EP12-RETRACT: {retraction_id}.retractedText must be a verbatim "
                f"fragment of at least {RETRACTION_MIN_FRAGMENT} characters; a "
                "one-character substring test is not a demonstration that the "
                "retraction targets the real bytes")
            continue
        if subject_file not in ALL_PINS:
            findings.append(f"EP12-RETRACT: {retraction_id}.subjectFile "
                            f"{subject_file!r} is not a pinned input")
            continue
        if subject_file.endswith(".py"):
            haystack = authority._snapshots[subject_file].decode("utf-8", "replace")
            located = "the pinned source"
        else:
            document = authority.json(subject_file)
            try:
                subject = _resolve_json_path(document, subject_path or "$")
            except MALFORMED:
                findings.append(f"EP12-RETRACT: {retraction_id}.subjectPath "
                                f"{subject_path!r} does not resolve in "
                                f"{subject_file}")
                continue
            if not isinstance(subject, str):
                findings.append(
                    f"EP12-RETRACT: {retraction_id}.subjectPath {subject_path!r} "
                    f"resolves to a {type(subject).__name__}, not to a string. A "
                    "retraction must name the CLAIM it withdraws, not the object "
                    "containing it: a fragment lifted from a different part of the "
                    "same object would otherwise satisfy this rule while the "
                    "retraction quoted nothing it retracts")
                continue
            haystack = subject
            located = f"{subject_file} at {subject_path}"
        if quoted not in haystack:
            findings.append(
                f"EP12-RETRACT: {retraction_id}.retractedText is not a verbatim "
                f"fragment of {located}; the retraction does not demonstrably "
                "target the bytes it names")
        statement = entry.get("statement") or ""
        if len(statement) < 200:
            findings.append(f"EP12-RETRACT: {retraction_id}.statement must say what "
                            "is false and what this run measured instead")

    for required in RETRACTION_CONTENT:
        entry = by_id.get(required) or {}
        statement = entry.get("statement") or ""
        for phrase in RETRACTION_CONTENT[required]:
            if phrase not in statement:
                findings.append(f"EP12-RETRACT: {required}.statement must state "
                                f"plainly that {phrase!r}")

    review = authority.json(EP11_REVIEW)
    if not isinstance(review, dict) or review.get("verdict") != "REJECT":
        findings.append("EP12-RETRACT: the pinned predecessor review must carry "
                        "verdict REJECT")
    blockers = review.get("blockers") if isinstance(review, dict) else None
    blocker_ids = sorted(item.get("id") for item in blockers) if isinstance(
        blockers, list) else []
    predecessor = contract.get("predecessor") or {}
    if predecessor.get("blockersAddressed") != blocker_ids:
        findings.append("EP12-RETRACT: predecessor.blockersAddressed is "
                        f"{predecessor.get('blockersAddressed')!r}; the pinned "
                        f"review carries {blocker_ids}")
    if predecessor.get("sha256") != ALL_PINS[EP11_ARTIFACT] or \
            predecessor.get("reviewSha256") != ALL_PINS[EP11_REVIEW] or \
            predecessor.get("checkerSha256") != ALL_PINS[EP11]:
        findings.append("EP12-RETRACT: predecessor must record the predecessor "
                        "artifact, its checker and its review by SHA-256")
    observations = review.get("nonBlockingObservations")
    observed_ids = sorted(item.get("id") for item in observations) if isinstance(
        observations, list) else []
    if predecessor.get("nonBlockingObservationsAddressed") != observed_ids:
        findings.append("EP12-RETRACT: predecessor.nonBlockingObservationsAddressed "
                        f"is {predecessor.get('nonBlockingObservationsAddressed')!r}; "
                        f"the pinned review carries {observed_ids}")
    return findings


# IR-EP11-NB-01: the predecessor enforced residuals by MINIMUM LENGTH plus a
# PHRASE GREP, and its reviewer gutted four of them — including the one carrying
# the whole threat-model concession — while the checker stayed green.  Padding
# satisfies a length test and the anchors survive any amount of hollowing.
#
# Here every residual must additionally BIND TO A MEASUREMENT OF THIS RUN.  Each
# declares a boundMeasurement naming a value this checker recomputes, and a
# boundValueText which must (a) equal that recomputed value rendered as text and
# (b) occur verbatim inside the residual's own prose.  Hollowing the prose drops
# the bound text and is a finding; editing the bound text disagrees with the run
# and is a finding; editing the measurement is impossible from the artifact.
#
# WHERE THAT CANNOT BE DONE IT IS SAID, not papered over.  A residual about the
# pre-existing failure of two OTHER checkers has no in-process measurement, so it
# is declared TEXT-ONLY-NOT-MECHANICALLY-ENFORCEABLE, that declaration is
# enforced against a list in THIS file rather than against the artifact, and the
# count of text-only residuals is published and printed in the banner.
RESIDUAL_BINDINGS = {
    "RES-EP12-01": (320, ("does NOT repair", "check-evaluation-proof-v6.py",
                          "OUTER gate"), "ep6Digest"),
    "RES-EP12-02": (520, ("ROUTE REGION", "own stack frame", "AX6", "RX2c",
                          "NOT closed", "enumeration"), "escapedEveryGuard"),
    "RES-EP12-03": (300, ("seven pinned vectors", "one distinct PlanIntent",
                          "value equality"), "answerPoints"),
    "RES-EP12-04": (260, ("tripwire", "supports NO published property"),
                    "tripwireBlindTo"),
    "RES-EP12-05": (200, ("own source", "not a verified snapshot"),
                    "ownSourceIsPinned"),
    "RES-EP12-06": (240, ("MEASURED, NOT REPAIRED", "canonical unsigned decimal",
                          "EP5 successor"), "ep5Digest"),
    "RES-EP12-07": (240, ("MEASURED, NOT REPAIRED", "durable identity",
                          "byte-identical", "v6/v8 successors"),
                    "identityMovingUnderSeal"),
    "RES-EP12-08": (200, ("14 intents", "not a proof"), "distinctIntentsDriven"),
    "RES-EP12-09": (240, ("rovenance is not correctness", "check-c2-v4.py"),
                    "repairedCheckerDigest"),
    "RES-EP12-10": (240, ("cannot re-run itself", "TOP-LEVEL run"), None),
    "RES-EP12-11": (300, ("pre-exist", "IR-C2V4-01", "rg"), None),
    "RES-EP12-12": (300, ("SOLE GUARD", "measured"), "soleGuardVariants"),
    "RES-EP12-13": (400, ("order-dependent", "deep-copies", "no guard mutated",
                          "the earlier review had nothing to catch"),
                    "sharedValuesMutated"),
    "RES-EP12-14": (240, ("asymmetric", "validate_plan_intent",
                          "plan_intent_commitment"), "oracleCases"),
    "RES-EP12-15": (400, ("IR-C2V4-01", "BLOCKING", "does not re-pin",
                          "admission API"), "repairedCheckerDigest"),
    "RES-EP12-16": (360, ("anchored window", "VALUE", "not by object identity"),
                    "unanchoredAgreements"),
    "RES-EP12-17": (300, ("text-only", "not mechanically enforceable"),
                    "residualEnforcement"),
}

# Residuals for which this instrument has NO in-process measurement to bind to.
# Declared HERE, in the checker, so the artifact cannot demote a bound residual
# to an unbound one.
TEXT_ONLY_RESIDUALS = ("RES-EP12-10", "RES-EP12-11")


def residual_measurements(heavy) -> dict[str, str]:
    """Every value a residual may bind to, recomputed from THIS run."""
    evasion = heavy["evasion"]
    answer = heavy["answerProvenance"]
    oracle = heavy["oracle"]
    delegate_heavy = heavy["delegate"]
    moving = [item for item in delegate_heavy["regimeB"]["admitted"]
              if item["classification"] == "type-distinct-one" and
              item["movedIdentities"]]
    under_seal = [item for item in moving
                  if "evaluationAuthoritySealRef" not in item["movedIdentities"]]
    blind = sorted(item["variant"] for item in evasion["tripwireOutcome"]
                   if not item["flagged"] and item["variant"] in DECLARED_ESCAPES)
    bound = sorted(set(RESIDUAL_BINDINGS) - set(TEXT_ONLY_RESIDUALS))
    return {
        "escapedEveryGuard": ", ".join(evasion["escapedEveryGuard"]),
        "tripwireBlindTo": ", ".join(blind),
        "answerPoints": (f"{answer['vectors']} pinned vectors x "
                         f"{answer['apisPerVector']} imported APIs = "
                         f"{answer['expectedPerRuleTotal']} answers"),
        "oracleCases": f"{oracle['stats']['executedCases']} enumerated cases",
        "identityMovingUnderSeal": (
            f"{len(under_seal)} of {len(moving)} identity-moving positions"),
        "distinctIntentsDriven": (
            f"{delegate_heavy['family']['distinctIntentsDriven']} distinct intents"),
        "repairedCheckerDigest": ALL_PINS[C2V4],
        "ep5Digest": ALL_PINS[EP5],
        "ep6Digest": ALL_PINS[EP6],
        "ownSourceIsPinned": f"own bytes in own pin table: {own_source_is_pinned()}",
        "soleGuardVariants": ", ".join(
            f"{item['variant']} ({item['soleGuard']})"
            for item in evasion["soleGuardVariants"]),
        "sharedValuesMutated": (
            f"{heavy['isolation']['casesDriven']} injections through "
            f"{heavy['isolation']['guardsDriven']} guards mutated "
            f"{heavy['isolation']['sharedValuesMutated']}"),
        "unanchoredAgreements": (
            f"{answer['unanchoredValueAgreements']} of "
            f"{answer['expectedPerRuleTotal']} unanchored answers"),
        "residualEnforcement": (
            f"{len(bound)} of {len(RESIDUAL_BINDINGS)} residuals bound to a "
            f"measurement, {len(TEXT_ONLY_RESIDUALS)} text-only"),
    }


def residual_checks(contract, heavy) -> list[str]:
    findings: list[str] = []
    limitations = contract.get("knownLimitations")
    if not isinstance(limitations, list):
        return ["EP12-RESIDUAL: knownLimitations must be an array"]
    measurements = residual_measurements(heavy)
    by_id: dict[str, dict] = {}
    for item in limitations:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            findings.append("EP12-RESIDUAL: every knownLimitations entry must be an "
                            "object carrying id, enforcement and text")
            continue
        by_id[item["id"]] = item
    for extra in sorted(set(by_id) - set(RESIDUAL_BINDINGS)):
        findings.append(f"EP12-RESIDUAL: knownLimitations carries {extra}, which "
                        "this checker does not enforce")
    measured_bound = 0
    for residual_id, (minimum, anchors, binding) in RESIDUAL_BINDINGS.items():
        entry = by_id.get(residual_id)
        if entry is None:
            findings.append(f"EP12-RESIDUAL: knownLimitations must carry "
                            f"{residual_id}; a declared residual may not be dropped")
            continue
        body = entry.get("text")
        if not isinstance(body, str):
            findings.append(f"EP12-RESIDUAL: {residual_id}.text must be a string")
            continue
        if len(body) < minimum:
            findings.append(
                f"EP12-RESIDUAL: {residual_id} is {len(body)} characters; a residual "
                f"must carry at least {minimum} characters of SUBSTANCE")
        for anchor in anchors:
            if anchor not in body:
                findings.append(f"EP12-RESIDUAL: {residual_id} must state "
                                f"{anchor!r}; its content, not its id, is the "
                                "disclosure")
        if residual_id in TEXT_ONLY_RESIDUALS:
            if entry.get("enforcement") != "TEXT-ONLY-NOT-MECHANICALLY-ENFORCEABLE":
                findings.append(
                    f"EP12-RESIDUAL: {residual_id} has no in-process measurement to "
                    "bind to and must declare enforcement="
                    "TEXT-ONLY-NOT-MECHANICALLY-ENFORCEABLE rather than a test that "
                    "would pass on hollow text")
            if entry.get("boundMeasurement") is not None:
                findings.append(f"EP12-RESIDUAL: {residual_id} is text-only and may "
                                "not claim a bound measurement")
            continue
        if entry.get("enforcement") != "MEASURED-BINDING":
            findings.append(f"EP12-RESIDUAL: {residual_id} must declare "
                            "enforcement=MEASURED-BINDING; this checker binds it to "
                            f"the measured value {binding!r}")
            continue
        if entry.get("boundMeasurement") != binding:
            findings.append(f"EP12-RESIDUAL: {residual_id} publishes "
                            f"boundMeasurement={entry.get('boundMeasurement')!r}; "
                            f"this checker binds it to {binding!r}")
            continue
        rendered = measurements.get(binding)
        bound_text = entry.get("boundValueText")
        if not strict_equal(bound_text, rendered):
            findings.append(
                f"EP12-RESIDUAL: {residual_id} publishes boundValueText="
                f"{bound_text!r}; this run measured {rendered!r}. A residual that "
                "does not carry what the run measured is a paragraph, not a "
                "disclosure")
            continue
        if bound_text not in body:
            findings.append(
                f"EP12-RESIDUAL: {residual_id}'s bound measurement {bound_text!r} "
                "does not occur in the residual's own text; hollowing the prose "
                "while keeping the anchors is exactly the defect "
                "ep11.review-independent.json IR-EP11-NB-01 demonstrated")
            continue
        measured_bound += 1
    published = contract.get("knownLimitationsEnforcement") or {}
    _expect(published, "declared", len(RESIDUAL_BINDINGS),
            "EP12-RESIDUAL: knownLimitationsEnforcement", findings)
    _expect(published, "boundToAMeasurement",
            len(RESIDUAL_BINDINGS) - len(TEXT_ONLY_RESIDUALS),
            "EP12-RESIDUAL: knownLimitationsEnforcement", findings)
    _expect(published, "textOnlyIds", sorted(TEXT_ONLY_RESIDUALS),
            "EP12-RESIDUAL: knownLimitationsEnforcement", findings)
    _expect(published, "bindingsSatisfiedThisRun", measured_bound,
            "EP12-RESIDUAL: knownLimitationsEnforcement", findings)
    return findings


ANSWER_RULE_IDS = ("A-1", "A-2", "A-3", "A-4", "A-5", "A-6", "A-7", "A-8")

ANSWER_COUNT_KEYS = (
    "vectors", "apisPerVector", "expectedPerRuleTotal",
    "independentValueAgreements", "anchoredObjectAgreements",
    "sharedLedgerAgreements", "repairedSentinelFlowed",
    "supersededSentinelIgnored", "gateAgreements", "installationIntact",
    "unanchoredValueAgreements", "recordParityHeld", "evaluationErrors")

ANCHOR_STATEMENT = (
    "the anchor is the FUNCTION OBJECT the SHA-256-verified bytes of "
    "check-c2-v4.py defined, read out of a module object this guard created by "
    "executing that snapshot inside answer_provenance_guard, at the instant that "
    "execution returned and before any route-region code could run against it. It "
    "is held in a local of the guard and in the closure of the servers the guard "
    "installs, is never bound to a module global, never stored on the Authority "
    "and never passed to the route region, and A-2 compares against it with `is`. "
    "A seat is a binding and can be written by anything that can name it; an "
    "anchor is an object and writing a binding does not change which object a "
    "local names. The server records the callee it ACTUALLY invoked, so a "
    "rewritten closure cell is reported rather than believed.")

SCOPE_STATEMENT = (
    "This property is established against a hostile ROUTE REGION. It is NOT "
    "established against a route region that reads or writes this guard's own "
    "stack frame, or the closure cells of the servers it installs: variants AX6, "
    "AX9 and RX2c do exactly that, are built and executed on every ordinary run, "
    "and are MEASURED to defeat every scored guard. The source tripwire that "
    "flags the cheap spellings of that class is an enumeration of identifiers and "
    "RX2c is measured to escape it, which is why the tripwire is not a scored "
    "guard and no published property depends on it.")


def verify_answer_provenance(contract, heavy) -> list[str]:
    findings: list[str] = []
    published = contract.get("answerProvenance") or {}
    counts = heavy["answerProvenance"]
    for key in ANSWER_COUNT_KEYS:
        _expect(published, key, counts[key], "EP12-ANSWER: answerProvenance",
                findings)
    for key in ("anchorsUnmoved", "anchorInstanceBindingsUnmoved"):
        _expect(published, key, counts[key], "EP12-ANSWER: answerProvenance",
                findings)
    if not counts.get("allRulesHeld"):
        findings.append("EP12-ANSWER: not every answer-provenance rule held over "
                        "every pinned vector and every imported API")
    if published.get("anchorStatement") != ANCHOR_STATEMENT:
        findings.append("EP12-ANSWER: answerProvenance.anchorStatement must state, "
                        "verbatim, WHAT the anchor is and why a binding the route "
                        "region can write is not one")
    if published.get("scopeStatement") != SCOPE_STATEMENT:
        findings.append("EP12-ANSWER: answerProvenance.scopeStatement must carry, "
                        "verbatim, the boundary this property is scoped by. A "
                        "property published without the scope that makes it true "
                        "is the failure mode this corpus keeps rejecting")
    rules = published.get("rules")
    if not isinstance(rules, list) or len(rules) != len(ANSWER_RULE_IDS):
        findings.append(f"EP12-ANSWER: answerProvenance.rules must publish "
                        f"{len(ANSWER_RULE_IDS)} rules, each stating the property "
                        "it establishes and the property it does not")
    else:
        declared = [item.get("id") for item in rules if isinstance(item, dict)]
        if declared != list(ANSWER_RULE_IDS):
            findings.append(f"EP12-ANSWER: answerProvenance.rules declares "
                            f"{declared}; this checker enforces "
                            f"{list(ANSWER_RULE_IDS)}")
        for item in rules:
            if not isinstance(item, dict):
                continue
            for field in ("establishes", "doesNotEstablish"):
                if not isinstance(item.get(field), str) or len(item[field]) < 40:
                    findings.append(
                        f"EP12-ANSWER: rule {item.get('id')!r} must state {field}; a "
                        "rule published without what it does NOT establish is the "
                        "defect ep10.review-independent.json found")
    if published.get("readsSource") is not False:
        findings.append("EP12-ANSWER: answerProvenance.readsSource must be false; "
                        "the load-bearing guard may not be a source scan")
    if published.get("establishesCallProvenanceOnly") is not False:
        findings.append("EP12-ANSWER: answerProvenance.establishesCallProvenanceOnly "
                        "must be false; that is the whole distinction from v10")
    if published.get("anchoredToTheSeat") is not False:
        findings.append(
            "EP12-ANSWER: answerProvenance.anchoredToTheSeat must be FALSE and "
            "published as such. The predecessor's rule was anchored to the module "
            "attribute the route region owns, which is IR-EP11-01")
    if published.get("isSoleGuardForAnswerProvenance") is not True:
        findings.append(
            "EP12-ANSWER: answerProvenance.isSoleGuardForAnswerProvenance must be "
            "TRUE and published as such; an undisclosed sole guard is IR-EP10-NB-05")

    control = heavy["control"]
    published_control = published.get("positiveControl") or {}
    if not strict_equal(published_control, control):
        findings.append("EP12-ANSWER: answerProvenance.positiveControl differs from "
                        "the control this run measured; the numbers that show the "
                        "guard still discriminates may not be edited")
    if not control["allProduceFindings"]:
        findings.append("EP12-ANSWER: a deliberately substituted join did not "
                        "produce an answer-provenance finding")
    decoy = control["decoyCall"]
    if decoy["independentValueAgreements"] != counts["expectedPerRuleTotal"]:
        findings.append(
            "EP12-ANSWER: the decoy control's A-1 agreement count is not the full "
            "total; A-1 is published as insufficient alone precisely because a "
            "substituted answer AGREES with it, and the control must show that")
    forged = control["forgedLedgerEntry"]
    if forged["sharedLedgerAgreements"] <= forged["anchoredObjectAgreements"]:
        findings.append(
            "EP12-ANSWER: the forged-ledger control does not show the shared "
            "served-module ledger agreeing where the anchored witness does not; "
            "without that difference the choice not to read the shared ledger is "
            "asserted rather than measured")
    seat = control["seatSubstitution"]
    if seat["installationIntact"]:
        findings.append(
            "EP12-ANSWER: the seat-substitution control did not move the load-time "
            "installation on this run; A-6 is then untested and the repair of "
            "IR-EP11-01 is unmeasured")
    return findings


def verify_predecessor_control(contract, heavy) -> list[str]:
    findings: list[str] = []
    published = contract.get("predecessorDefeatControl") or {}
    measured = heavy["predecessor"]
    if not strict_equal(published, measured):
        findings.append(
            "EP12-PREDECESSOR: predecessorDefeatControl differs from the control "
            "this run measured. This block is the ONLY evidence that the defect "
            "being repaired exists in the predecessor's own bytes and that this "
            "instrument sees it, and it may not be edited")
    return findings


def verify_call_provenance(contract, heavy) -> list[str]:
    findings: list[str] = []
    published = contract.get("callProvenance") or {}
    measure = heavy["callProvenance"]
    for key in ("vectorsDriven", "distinctIntentsDriven", "observedCalls",
                "depthZeroCalls", "distinctFingerprintsObserved",
                "supersededCallsInsideJoin"):
        _expect(published, key, measure[key], "EP12-CALL: callProvenance", findings)
    if published.get("readsSource") is not False:
        findings.append("EP12-CALL: callProvenance.readsSource must be false")
    statement = published.get("whatThisEstablishes") or ""
    for phrase in ("which module was CALLED",):
        if phrase not in statement:
            findings.append(f"EP12-CALL: callProvenance.whatThisEstablishes must say "
                            f"{phrase!r} in terms")
    negative = published.get("whatThisDoesNotEstablish") or ""
    for phrase in ("not whose answer was used", "discarded"):
        if phrase not in negative:
            findings.append(
                f"EP12-CALL: callProvenance.whatThisDoesNotEstablish must say "
                f"{phrase!r}")
    if published.get("isSufficientAlone") is not False:
        findings.append("EP12-CALL: callProvenance.isSufficientAlone must be false")
    return findings


# IR-EP11-NB-05: the predecessor's inventory said "every guard this instrument
# runs is listed here" and listed only the six the evasion matrix scores, while
# at least seven other finding-producing mechanisms ran.  Here the inventory must
# list EVERY mechanism that can produce a finding, each declaring whether the
# evasion matrix scores it; and sole-guard status is published as a boolean only
# where it is MEASURED, and as null where it is not.
GUARD_REGISTRY = (
    ("answerProvenance", True),
    ("callProvenance", True),
    ("differentialOracle", True),
    ("supersededCrossCheck", True),
    ("c2RouteScan", True),
    ("introspectionTripwire", False),
    ("c2ApiSurface", False),
    ("globalBindingProbe", False),
    ("injectionIsolationProbe", False),
    ("predecessorDefeatControl", False),
    ("positiveControl", False),
    ("predecessorCheckingLayer", False),
    ("ownConstantLeafBattery", False),
    ("exitMatrixProbe", False),
    ("selftestDispatchScan", False),
    ("integerGuardScan", False),
    ("nonCircularityScan", False),
    ("pinAgreement", False),
    ("residualAndRetractionBinding", False),
)

GUARD_INVENTORY_WHY = (
    "IR-EP11-NB-05: the predecessor's inventory claimed to list every guard the "
    "instrument runs and listed only the six the evasion matrix scored, omitting "
    "c2_api_surface entirely. This inventory lists EVERY mechanism in this file "
    "that can produce a finding, says for each whether the evasion matrix scores "
    "it, and publishes sole-guard status as a measured boolean only where it is "
    "measured and as null where it is not. An inventory that claims completeness "
    "and is not complete is the failure mode of IMPLEMENTATION-FREEZE 7 applied "
    "to the inventory itself.")


def verify_guard_inventory(contract, heavy) -> list[str]:
    findings: list[str] = []
    inventory = contract.get("guardInventory") or {}
    guards = inventory.get("guards")
    if not isinstance(guards, list):
        return ["EP12-INVENTORY: guardInventory.guards must be an array"]
    declared = {item.get("id"): item for item in guards if isinstance(item, dict)}
    registry = dict(GUARD_REGISTRY)
    if sorted(declared) != sorted(registry):
        findings.append(f"EP12-INVENTORY: guardInventory declares {sorted(declared)}; "
                        f"this checker runs {sorted(registry)}")
    if inventory.get("why") != GUARD_INVENTORY_WHY:
        findings.append("EP12-INVENTORY: guardInventory.why must carry, verbatim, "
                        "the statement of what this inventory covers")
    evasion = heavy["evasion"]
    sole_guards = {item["soleGuard"] for item in evasion["soleGuardVariants"]}
    for item in guards:
        if not isinstance(item, dict):
            continue
        guard_id = item.get("id")
        for field in ("establishes", "blindSpot", "readsSource",
                      "scoredByEvasionMatrix", "isSoleGuardForSomeClass"):
            if field not in item:
                findings.append(f"EP12-INVENTORY: guard {guard_id!r} must publish "
                                f"{field}")
        if guard_id not in registry:
            continue
        expected_source = guard_id in SOURCE_READING_GUARDS or \
            guard_id in ("introspectionTripwire", "selftestDispatchScan",
                         "integerGuardScan", "nonCircularityScan")
        if not strict_equal(item.get("readsSource"), expected_source):
            findings.append(f"EP12-INVENTORY: guard {guard_id!r} publishes "
                            f"readsSource={item.get('readsSource')!r}; this checker "
                            f"runs it as readsSource={expected_source}")
        if not strict_equal(item.get("scoredByEvasionMatrix"), registry[guard_id]):
            findings.append(f"EP12-INVENTORY: guard {guard_id!r} publishes "
                            "scoredByEvasionMatrix="
                            f"{item.get('scoredByEvasionMatrix')!r}; this run "
                            f"scores it {registry[guard_id]}")
        if isinstance(item.get("blindSpot"), str) and len(item["blindSpot"]) < 60:
            findings.append(f"EP12-INVENTORY: guard {guard_id!r} publishes a "
                            "blind spot too short to be a disclosure; every guard "
                            "has one and a claim of total coverage is a finding")
        if registry[guard_id]:
            if not strict_equal(item.get("isSoleGuardForSomeClass"),
                                guard_id in sole_guards):
                findings.append(f"EP12-INVENTORY: guard {guard_id!r} publishes "
                                "isSoleGuardForSomeClass="
                                f"{item.get('isSoleGuardForSomeClass')!r}; this run "
                                f"measured {guard_id in sole_guards}")
        elif item.get("isSoleGuardForSomeClass") is not None:
            findings.append(
                f"EP12-INVENTORY: guard {guard_id!r} is NOT scored by the evasion "
                "matrix, so whether it is a sole catcher for any class is "
                "UNMEASURED and must be published as null rather than as a boolean "
                "nothing on this run established")
    _expect(inventory, "perGuardCatchCount", evasion["perGuardCatchCount"],
            "EP12-INVENTORY: guardInventory", findings)
    _expect(inventory, "soleGuardVariants", evasion["soleGuardVariants"],
            "EP12-INVENTORY: guardInventory", findings)
    _expect(inventory, "answerProvenanceOnlyCatches",
            evasion["answerProvenanceOnlyCatches"],
            "EP12-INVENTORY: guardInventory", findings)
    if inventory.get("claimsTotalCoverage") is not False:
        findings.append("EP12-INVENTORY: guardInventory.claimsTotalCoverage must be "
                        "false; an inventory that claims total coverage is refused")
    for guard_id in sorted(sole_guards):
        item = declared.get(guard_id) or {}
        if item.get("isSoleGuardForSomeClass") is not True:
            findings.append(
                f"EP12-INVENTORY: guard {guard_id!r} is the SOLE catcher for "
                f"{[row['variant'] for row in evasion['soleGuardVariants'] if row['soleGuard'] == guard_id]} "
                "in this run and must publish isSoleGuardForSomeClass=true")
    return findings


REQUIRED_EVASIONS = (
    "AX2-decoy-call-superseded-answer", "AX3-verdict-only-substitution",
    "AX4-commitment-only-substitution", "AX5-probe-family-split-answers",
    "AX6-stack-walking-witness-forgery", "AX8-differential-sentinel-detector",
    "AX9-obfuscated-witness-forgery", "RX2c-unenumerated-witness-forgery",
    "RX1-seat-substitution-declared-accessor",
    "RX3-seat-wrapping-of-the-guards-own-server",
    "RX4-stale-anchored-object-replay",
    "RX6-seat-substitution-module-accessor",
    "RX5-seat-rebind-before-capture",
    "forged-ledger-entry-replay",
    "R1-probe-whitelist-direct-module", "R4-probe-whitelist-accessor-routed",
    "tag-forgery-at-install", "superseded-backed-shim", "monkeypatched-recorder",
    "getattr-proxy-accessor", "unwrapped-module", "deinstalled-ledger",
    "poisoned-accessor",
)

# Variants that substitute the ANSWER while leaving the CALLS honest.  Every one
# of them is green under all of v10's ledger rules; the answer-provenance guard
# must catch every one or IR-EP10-01 is unrepaired.
ANSWER_SUBSTITUTION_VARIANTS = (
    "AX2-decoy-call-superseded-answer", "AX3-verdict-only-substitution",
    "AX4-commitment-only-substitution", "AX5-probe-family-split-answers",
    "AX8-differential-sentinel-detector", "forged-ledger-entry-replay",
)

# Variants that rebind, wrap, replace or replay the SEAT — the class
# ep11.review-independent.json found blocking.  Each must be caught by the
# answer-provenance guard or IR-EP11-01 is unrepaired.
SEAT_SUBSTITUTION_VARIANTS = (
    "RX1-seat-substitution-declared-accessor",
    "RX3-seat-wrapping-of-the-guards-own-server",
    "RX4-stale-anchored-object-replay",
    "RX6-seat-substitution-module-accessor",
    "RX5-seat-rebind-before-capture",
)

# Variants that tamper with the GUARD'S OWN FRAME rather than with the route.
# These are OUTSIDE the published property's declared scope (RES-EP12-02); they
# are built and executed anyway and they are DECLARED to escape.
GUARD_TAMPER_VARIANTS = ("AX6-stack-walking-witness-forgery",
                         "AX9-obfuscated-witness-forgery",
                         "RX2c-unenumerated-witness-forgery")

# Variants declared IN ADVANCE to escape every scored guard.  Measured; if this
# set and the measured escape set disagree in EITHER direction it is a finding.
DECLARED_ESCAPES = GUARD_TAMPER_VARIANTS

# The tripwire is expected to be BLIND to this one.  Measured, and a finding if
# the measurement disagrees in either direction, so that the enumeration's
# limitation is a published number rather than a paragraph.
TRIPWIRE_BLIND_VARIANTS = ("RX2c-unenumerated-witness-forgery",)


def verify_evasion(contract, heavy) -> list[str]:
    findings: list[str] = []
    published = contract.get("evasionMeasurement") or {}
    evasion = heavy["evasion"]
    for key in ("variantsDeclared", "variantsBuilt", "sourceVariantsBuilt",
                "objectAttacksBuilt", "caughtByAtLeastOneGuard",
                "escapedEveryGuard"):
        _expect(published, key, evasion[key], "EP12-EVASION: evasionMeasurement",
                findings)
    if not strict_equal(published.get("perVariant"), evasion["perVariant"]):
        findings.append("EP12-EVASION: evasionMeasurement.perVariant differs from "
                        "the per-guard catch matrix this run measured; the "
                        "unflattering per-variant result may not be edited")
    if not strict_equal(published.get("tripwireOutcome"),
                        evasion["tripwireOutcome"]):
        findings.append("EP12-EVASION: evasionMeasurement.tripwireOutcome differs "
                        "from the tripwire verdicts this run measured")
    built = {item["variant"] for item in evasion["perVariant"]}
    for required in REQUIRED_EVASIONS:
        if required not in built:
            findings.append(f"EP12-EVASION: the required evasion {required!r} was "
                            "not built")
            continue
        item = next(row for row in evasion["perVariant"]
                    if row["variant"] == required)
        if required in ANSWER_SUBSTITUTION_VARIANTS and not item["answerProvenance"]:
            findings.append(
                f"EP12-EVASION: {required} substitutes the ANSWER and the "
                "answer-provenance guard did not catch it; that is the blocking "
                "finding of ep10.review-independent.json, unrepaired")
        if required in SEAT_SUBSTITUTION_VARIANTS and not item["answerProvenance"]:
            findings.append(
                f"EP12-EVASION: {required} rebinds, wraps, replaces or replays the "
                "SEAT and the answer-provenance guard did not catch it; that is the "
                "blocking finding of ep11.review-independent.json, unrepaired")
    escaped = evasion["escapedEveryGuard"]
    if sorted(escaped) != sorted(DECLARED_ESCAPES):
        findings.append(
            f"EP12-EVASION: the measured escape set {escaped} is not the declared "
            f"escape set {sorted(DECLARED_ESCAPES)}. A declared escape that does "
            "not escape flatters the declaration; an undeclared escape is a "
            "coverage claim over a class this run measured itself failing")
    _expect(published, "declaredBlindSpotVariants", sorted(DECLARED_ESCAPES),
            "EP12-EVASION: evasionMeasurement", findings)
    blind = {item["variant"] for item in evasion["tripwireOutcome"]
             if not item["flagged"]}
    for name in TRIPWIRE_BLIND_VARIANTS:
        if name not in blind:
            findings.append(
                f"EP12-EVASION: the introspection tripwire FLAGGED {name!r} on this "
                "run. That variant exists to measure that the enumeration is not a "
                "proof; if the enumeration now names it, the measurement has been "
                "lost and a new unenumerated spelling must be built")
    for name in GUARD_TAMPER_VARIANTS:
        item = next((row for row in evasion["perVariant"]
                     if row["variant"] == name), None)
        if item is None:
            findings.append(f"EP12-EVASION: the guard-tamper variant {name!r} must "
                            "be BUILT AND EXECUTED, not asserted")
            continue
        if item["answerProvenance"]:
            findings.append(
                f"EP12-EVASION: {name!r} is declared OUT OF SCOPE and published as "
                "an escape, but this run caught it. Either the scope statement is "
                "understated or the variant no longer performs the tamper it names")
    tamper = [{"variant": name,
               "caughtBy": [key for key in GUARD_IDS
                            if next(row for row in evasion["perVariant"]
                                    if row["variant"] == name)[key]],
               "flaggedByTripwire": next(
                   row["flagged"] for row in evasion["tripwireOutcome"]
                   if row["variant"] == name),
               "defeatsAnswerProvenance": True}
              for name in GUARD_TAMPER_VARIANTS if name in built]
    _expect(published, "guardTamperOutcome", tamper,
            "EP12-EVASION: evasionMeasurement", findings)
    if published.get("escapeSetIsAMeasurementNotACoverageClaim") is not True:
        findings.append("EP12-EVASION: evasionMeasurement must declare that the "
                        "escape set is a measurement over the classes built here "
                        "and not a coverage claim over the space of evasions")
    return findings


def verify_scans(contract, heavy, counterparts) -> list[str]:
    findings: list[str] = []
    scope = contract.get("astScanScope") or {}
    route = c2_route_scan()
    introspection = route_introspection_scan()
    dispatch = selftest_dispatch_scan()
    integers = integer_guard_scan()
    circular = non_circularity_scan()
    if route["referencesOutsideDeclaredClosure"]:
        findings.append("EP12-SCAN: a C-2 API is named outside the declared join "
                        "and measurement closure: "
                        f"{route['referencesOutsideDeclaredClosure']}")
    if route["unroutedSitesInsideJoin"]:
        findings.append("EP12-SCAN: a C-2 call inside the join does not route "
                        f"through an Authority accessor: "
                        f"{route['unroutedSitesInsideJoin']}")
    if route["authorityRoutedSites"] < len(C2_IMPORTED_APIS):
        findings.append(f"EP12-SCAN: only {route['authorityRoutedSites']} "
                        "accessor-routed C-2 site(s) remain inside the join")
    if introspection["introspectionSites"]:
        findings.append("EP12-SCAN: the route region names an introspection "
                        f"primitive: {introspection['introspectionSites']}; the "
                        "route region reads its arguments, not the guard")
    if dispatch["selftestCalls"] != 1 or dispatch["mainFunctions"] != 1 or \
            not dispatch["dispatchBeforeFindings"]:
        findings.append("EP12-SCAN: the selftest dispatch is not unique, live and "
                        f"positioned before any findings return: {dispatch}")
    if integers["bareNumericComparisons"]:
        findings.append("EP12-SCAN: a bare numeric comparison against a literal "
                        "remains in a wire-sourced position — this is the LB-C2-01 "
                        f"class: {integers['bareNumericComparisons']}")
    if circular["literalsThatAreNotPins"]:
        findings.append("EP12-SCAN: this checker's own text carries 64-hex "
                        f"literal(s) that are not pins: "
                        f"{circular['literalsThatAreNotPins']}; a commitment or "
                        "identity literal in the instrument makes it circular")
    published_circular = scope.get("nonCircularity") or {}
    for key in ("uniqueHexLiterals", "pinnedDigests", "literalsThatAreNotPins"):
        _expect(published_circular, key, circular[key],
                "EP12-SCAN: astScanScope.nonCircularity", findings)
    _expect(scope, "introspectionEnumeratedSpellings",
            introspection["enumeratedSpellings"], "EP12-SCAN: astScanScope",
            findings)
    if scope.get("noPublishedPropertyRestsOnAnEnumeration") is not True:
        findings.append(
            "EP12-SCAN: astScanScope.noPublishedPropertyRestsOnAnEnumeration must "
            "be true and must be MEASURED: the introspection tripwire is excluded "
            "from the scored guard set and the class it used to be the sole catcher "
            "of is published as a declared, measured escape")

    declared_scans = scope.get("scans")
    if not isinstance(declared_scans, list):
        return findings + ["EP12-SCAN: astScanScope.scans must be an array"]
    declared = {item.get("id"): item for item in declared_scans
                if isinstance(item, dict)}
    measured_ids = [item[0] for item in AST_SCAN_REGISTRY]
    if sorted(declared) != sorted(measured_ids):
        findings.append(f"EP12-SCAN: astScanScope.scans declares {sorted(declared)}; "
                        f"this checker runs {sorted(measured_ids)}")
    sole_guard = []
    for scan_id, guarded_property, counterpart in AST_SCAN_REGISTRY:
        item = declared.get(scan_id) or {}
        if item.get("isTripwire") is not True:
            findings.append(f"EP12-SCAN: scan {scan_id} must declare isTripwire=true")
        if item.get("guardedProperty") != guarded_property:
            findings.append(f"EP12-SCAN: scan {scan_id} publishes guardedProperty="
                            f"{item.get('guardedProperty')!r}; this checker guards "
                            f"{guarded_property!r}")
        if item.get("behaviouralCounterpart") != counterpart:
            findings.append(f"EP12-SCAN: scan {scan_id} publishes "
                            "behaviouralCounterpart="
                            f"{item.get('behaviouralCounterpart')!r}; this checker "
                            f"runs {counterpart!r}")
        if not counterparts.get(scan_id):
            sole_guard.append(scan_id)
    _expect(scope, "astOnlyProperties", sole_guard, "EP12-SCAN: astScanScope",
            findings)
    if sole_guard:
        findings.append(f"EP12-SCAN: {sole_guard} has NO executed behavioural "
                        "counterpart in this run; no source scan may be the sole "
                        "guard for any property")
    if scope.get("isSoleGuardForAnyProperty") is not False:
        findings.append("EP12-SCAN: astScanScope.isSoleGuardForAnyProperty must be "
                        "false and must be measured, not asserted")
    if scope.get("routingScanCannotSeeWhichModuleServes") is not True:
        findings.append("EP12-SCAN: astScanScope must declare that the routing scan "
                        "cannot see WHICH MODULE serves a call")
    if scope.get("routingScanCannotSeeWhoseAnswerIsUsed") is not True:
        findings.append("EP12-SCAN: astScanScope must declare that NO source scan "
                        "can see whose ANSWER the join used; that is the property "
                        "the answer-provenance guard exists for")
    return findings


def verify_totality(contract, heavy, root_census) -> list[str]:
    findings: list[str] = []
    published = contract.get("scalarLeafTotality") or {}
    declared = {item.get("surface"): item
                for item in (published.get("surfaces") or [])
                if isinstance(item, dict)}
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
        entry = declared.get(name)
        if entry is None:
            findings.append(f"EP12-TOTALITY: surface {name} is not published")
            continue
        for key in ("enumeratedPaths", "containerPaths", "scalarLeafPaths"):
            _expect(entry, key, item["census"][key],
                    f"EP12-TOTALITY: surface {name}", findings)
        for key in ("enumeratedCases", "noOpInjections", "executedCases",
                    "guardedEscapes", "silentAccepts"):
            _expect(entry, key, item["stats"][key],
                    f"EP12-TOTALITY: surface {name}", findings)
        # IR-EP10-NB-03: a count is not a record.
        _expect(entry, "silentAcceptPositions", item["silent"],
                f"EP12-TOTALITY: surface {name}", findings)
        if len(item["silent"]) != item["stats"]["silentAccepts"]:
            findings.append(f"EP12-TOTALITY: surface {name} enumerated "
                            f"{len(item['silent'])} silently-accepted position(s) "
                            f"but counted {item['stats']['silentAccepts']}")
        if item["stats"]["guardedEscapes"]:
            findings.append(f"EP12-TOTALITY: surface {name} produced "
                            f"{item['stats']['guardedEscapes']} guarded escapes")
    for name in sorted(set(declared) - set(measured)):
        findings.append(f"EP12-TOTALITY: the candidate publishes surface {name}, "
                        "which this run does not measure")
    root = published.get("contractRoot") or {}
    for key in ("enumeratedPaths", "containerPaths", "scalarLeafPaths", "dictPaths",
                "listPaths"):
        _expect(root, key, root_census[key], "EP12-TOTALITY: contractRoot", findings)
    _expect(published, "injectionValues", len(HOSTILE_VALUES),
            "EP12-TOTALITY: scalarLeafTotality", findings)
    if published.get("understatingIsAFinding") is not True:
        findings.append("EP12-TOTALITY: scalarLeafTotality.understatingIsAFinding "
                        "must remain true")
    surface = published.get("evaluationAuthorityCandidateSurface") or {}
    _expect(surface, "regimeAScalarLeafPaths",
            heavy["delegate"]["regimeA"]["scalarLeafPaths"],
            "EP12-TOTALITY: evaluationAuthorityCandidateSurface", findings)
    _expect(surface, "regimeBScalarLeafPaths",
            heavy["delegate"]["regimeB"]["scalarLeafPaths"],
            "EP12-TOTALITY: evaluationAuthorityCandidateSurface", findings)
    isolation = published.get("injectionIsolation") or {}
    for key in ("guardsDriven", "casesDriven", "mutableTableMembers",
                "sharedValuesMutated", "injectorDeepCopies"):
        _expect(isolation, key, heavy["isolation"][key],
                "EP12-TOTALITY: injectionIsolation", findings)
    return findings


PRESERVATION_METHOD = (
    "check-evaluation-proof-v10.py is pinned by SHA-256, read once as inert bytes, "
    "verified, and EXECUTED from that verified in-memory snapshot. The measurements "
    "ep10.review-independent.json verified by independent re-derivation, and "
    "ep11.review-independent.json re-verified by executing v10 itself, are neither "
    "transcribed nor rebuilt: they are produced here by the same bytes, and the "
    "pinned v10 candidate is additionally driven through v10's own checking layer "
    "on this run and required to produce zero findings. The REJECTED predecessor "
    "v11 is deliberately not delegated to and its checking layer is not run here: "
    "it exits 0 on its own candidate while that candidate publishes the property "
    "RET-EP12-01 retracts, and executing it would republish a retracted green.")

ADMISSION_DESCRIPTOR_POSITION = (
    "$.admittedResolvedInputs.frozenPlanIntent.analysis.admissionDescriptor."
    "schemaVersion=json-true")


def verify_preserved(contract, heavy) -> list[str]:
    """The reviewer-verified v10 measurements, reproduced by EXECUTION."""
    findings: list[str] = []
    published = contract.get("preservedMeasurements") or {}
    delegate_heavy = heavy["delegate"]
    if published.get("method") != PRESERVATION_METHOD:
        findings.append("EP12-PRESERVED: preservedMeasurements.method must state "
                        "that the predecessor's verified bytes are EXECUTED rather "
                        "than transcribed, and why v11 is not delegated to")
    _expect(published, "predecessorCheckingLayerFindings", len(heavy["v10Findings"]),
            "EP12-PRESERVED: preservedMeasurements", findings)
    if heavy["delegateSourceSealed"] is not True:
        findings.append("EP12-PRESERVED: the delegate's self-source cache was not "
                        "seeded with the verified bytes, so the delegate would "
                        "re-read its own path; the trust order is broken")
    _expect(published, "delegateSourceCacheSeeded", heavy["delegateSourceSealed"],
            "EP12-PRESERVED: preservedMeasurements", findings)

    for label in ("A", "B"):
        block = (published.get("regimes") or {}).get(label)
        measured = delegate_heavy["regime" + label]
        if not isinstance(block, dict):
            findings.append(f"EP12-PRESERVED: regime {label} is not published")
            continue
        for key in ("regime", "enumeratedPaths", "containerPaths",
                    "scalarLeafPaths", "executedCases", "noOpInjections",
                    "rejectedCount", "admittedCount"):
            _expect(block, key, measured[key], f"EP12-PRESERVED: regime {label}",
                    findings)
        if not strict_equal(block, measured):
            findings.append(f"EP12-PRESERVED: regime {label} as published is not "
                            "the block this run re-derived by execution")
        if not strict_equal(block.get("admitted"), measured["admitted"]):
            findings.append(f"EP12-PRESERVED: regime {label}'s admitted set differs "
                            "from the set this run re-derived by execution")
        if not strict_equal(block.get("baseline"), measured["baseline"]):
            findings.append(f"EP12-PRESERVED: regime {label} publishes a baseline "
                            "identity set this run did not recompute")
    moving = [item for item in delegate_heavy["regimeB"]["admitted"]
              if item["classification"] == "type-distinct-one" and
              item["movedIdentities"]]
    under_seal = [item for item in moving
                  if "evaluationAuthoritySealRef" not in item["movedIdentities"]]
    _expect(published, "identityMovingPositions", len(moving),
            "EP12-PRESERVED: preservedMeasurements", findings)
    _expect(published, "identityMovingUnderByteIdenticalSeal", len(under_seal),
            "EP12-PRESERVED: preservedMeasurements", findings)
    if not under_seal:
        findings.append("EP12-PRESERVED: no producer-consistent position was "
                        "measured that moves durable identity beneath a "
                        "byte-identical EvaluationAuthoritySealRef")
    admitted_b = {item["position"] for item in delegate_heavy["regimeB"]["admitted"]}
    if ADMISSION_DESCRIPTOR_POSITION not in admitted_b:
        findings.append("EP12-PRESERVED: the admissionDescriptor.schemaVersion "
                        "position the ep10 review independently confirmed is not in "
                        "this run's regime-B admitted set")

    stability = delegate_heavy["stability"]
    published_stability = published.get("planIntentCommitmentStability") or {}
    for key in ("vectors", "recomputedUnderV4", "reproducedUnderSupersededEncoder",
                "preimageByteIdentical", "distinctCommitments",
                "preimageByteLengths", "distinctFrozenPlanIntents",
                "distinctPlanDescriptors"):
        _expect(published_stability, key, stability[key],
                "EP12-PRESERVED: planIntentCommitmentStability", findings)
    family = delegate_heavy["family"]
    published_family = published.get("distinctIntentFamily") or {}
    for key in ("declaredPerturbations", "acceptedByRepairedInstrument",
                "distinctIntentsDriven", "rejectedPerturbations",
                "distinctCommitments", "injective",
                "reproducedUnderSupersededEncoder", "preimageByteIdentical"):
        _expect(published_family, key, family[key],
                "EP12-PRESERVED: distinctIntentFamily", findings)
    if not family["injective"]:
        findings.append("EP12-PRESERVED: the repaired encoder did not map the "
                        "distinct PlanIntent family injectively")
    probe = delegate_heavy["probe"]
    published_probe = published.get("lbC201ProbeFamily") or {}
    for key in ("cases", "repairedAdmitted", "supersededAdmitted", "secondDigests",
                "admitThenRaise", "discriminatingCardinality",
                "supersededAdmittedDerivedExpectation"):
        _expect(published_probe, key, probe[key],
                "EP12-PRESERVED: lbC201ProbeFamily", findings)
    if probe["repairedAdmitted"]:
        findings.append(f"EP12-PRESERVED: the repaired instrument admitted "
                        f"{probe['repairedAdmitted']} type-distinct case(s)")
    published_v10_evasion = published.get("predecessorEvasionBattery") or {}
    for key in ("caughtByAstTripwire", "missedByAstTripwire",
                "caughtByDifferentialOracle", "missedByDifferentialOracle",
                "caughtByRoutingLedger", "variantsBuilt"):
        _expect(published_v10_evasion, key, delegate_heavy["evasion"][key],
                "EP12-PRESERVED: predecessorEvasionBattery", findings)
    return findings


def check(contract: Any, authority: Authority, snapshots) -> list[str]:
    findings: list[str] = []
    if not isinstance(contract, dict):
        return ["EP12-SHAPE: the candidate must be a JSON object"]

    if contract.get("artifact") != "opensip.evaluation-proof":
        findings.append("EP12-SHAPE: artifact must be opensip.evaluation-proof")
    _exact_int(contract.get("version"), "version", findings, EXPECTED_VERSION)
    if contract.get("status") != "CANDIDATE-NOT-APPLIED":
        findings.append("EP12-POSTURE: status must remain CANDIDATE-NOT-APPLIED")
    if contract.get("reviewState") != "AWAITING-INDEPENDENT-REVIEW":
        findings.append("EP12-POSTURE: reviewState must remain "
                        "AWAITING-INDEPENDENT-REVIEW")
    if contract.get("sealRecommendation") != "DO-NOT-SEAL":
        findings.append("EP12-POSTURE: sealRecommendation must remain DO-NOT-SEAL")
    assurance = contract.get("assurance") or {}
    if assurance.get("state") != "SPECIFIED" or \
            assurance.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED" or \
            assurance.get("candidateState") != "NOT-APPLIED":
        findings.append("EP12-POSTURE: assurance must remain SPECIFIED / "
                        "IMPLEMENTABLE_UNEXECUTED / NOT-APPLIED")
    if assurance.get("qualificationEvidenceIds") or \
            assurance.get("releaseEvidenceIds"):
        findings.append("EP12-POSTURE: no qualification or release evidence may be "
                        "claimed by a CANDIDATE-NOT-APPLIED artifact")
    document = json.dumps(contract, sort_keys=True, ensure_ascii=False)
    for forbidden in ("DISCHARGED", "DEMONSTRATED-AND-SEALED", "SIGNED-OFF"):
        if forbidden in document:
            findings.append(f"EP12-POSTURE: the candidate contains {forbidden!r}; "
                            "implementable is not discharged")
    if "CD-RT-5" not in document or "BLOCKED_ON_PHASE_1A" not in document:
        findings.append("EP12-POSTURE: CD-RT-5 must remain named, unsigned and "
                        "recorded as BLOCKED_ON_PHASE_1A")
    claim = contract.get("cdRt5") or {}
    if claim.get("claim") != "CD-RT-5" or \
            claim.get("status") != "BLOCKED_ON_PHASE_1A" or \
            claim.get("signed") is not False:
        findings.append("EP12-POSTURE: cdRt5 must record claim CD-RT-5, status "
                        "BLOCKED_ON_PHASE_1A and signed=false; no lane here may "
                        "move it and a boolean nobody checks is not a record")

    repair_join = contract.get("c2AuthorityRepairJoin") or {}
    residual = repair_join.get("ep6InnerJoinResidual")
    if repair_join.get("ep6InnerJoinResidualId") != "RES-EP12-01":
        findings.append("EP12-RESIDUAL: c2AuthorityRepairJoin.ep6InnerJoinResidualId "
                        "must be RES-EP12-01")
    if not isinstance(residual, str) or "does not repair" not in residual or \
            "check-evaluation-proof-v6.py" not in residual:
        findings.append("EP12-RESIDUAL: c2AuthorityRepairJoin.ep6InnerJoinResidual "
                        "must state that v12 does not repair "
                        "check-evaluation-proof-v6.py")

    heavy = heavy_measurements(authority, snapshots)
    findings += list(heavy["findings"])
    if not heavy["named"]:
        return findings

    findings += residual_checks(contract, heavy)
    findings += pin_agreement(contract, authority)
    findings += retraction_checks(contract, authority)

    source_artifact = authority.json(VECTOR_SOURCE)
    if (authority.json(EP9_ARTIFACT) or {}).get("positiveVectors") != \
            source_artifact.get("positiveVectors"):
        findings.append("EP12-VECTORS: the rejected evaluation-proof.v9.json's "
                        "positiveVectors differ from the PASSED EP8 artifact's; "
                        "v12 takes its vectors from EP8 and requires them to agree")
    for rejected in (EP9_ARTIFACT, EP10_ARTIFACT, EP11_ARTIFACT):
        declared = ((authority.json(rejected) or {}).get("c2AuthorityJoin")
                    or {}).get("expectedPlanIntentCommitment")
        if declared != (source_artifact.get("c2AuthorityJoin") or {}).get(
                "expectedPlanIntentCommitment"):
            findings.append(f"EP12-VECTORS: {rejected} declares a PlanIntent "
                            "commitment that differs from the PASSED EP8 "
                            "artifact's; the chain's subject has moved")

    findings += verify_answer_provenance(contract, heavy)
    findings += verify_predecessor_control(contract, heavy)
    findings += verify_call_provenance(contract, heavy)
    findings += verify_guard_inventory(contract, heavy)
    findings += verify_evasion(contract, heavy)
    findings += verify_preserved(contract, heavy)

    oracle = heavy["oracle"]
    published_oracle = contract.get("differentialOracle") or {}
    _expect(published_oracle, "executedCases", oracle["stats"]["executedCases"],
            "EP12-DIFF: differentialOracle", findings)
    _expect(published_oracle, "joinVsRepairedMismatches",
            oracle["stats"]["joinVsRepairedMismatches"],
            "EP12-DIFF: differentialOracle", findings)
    _expect(published_oracle, "discriminatingCardinality",
            oracle["discriminatingCardinality"], "EP12-DIFF: differentialOracle",
            findings)
    _expect(published_oracle, "discriminatingPositions", oracle["firstDivergent"],
            "EP12-DIFF: differentialOracle", findings)
    if published_oracle.get("isSufficientAlone") is not False:
        findings.append("EP12-DIFF: differentialOracle.isSufficientAlone must be "
                        "false; it is an A-1-shaped instrument and every "
                        "answer-substitution variant agrees with it")
    if published_oracle.get("computedOnPrivateInstance") is not True:
        findings.append("EP12-DIFF: differentialOracle.computedOnPrivateInstance "
                        "must be true; a reference answer taken through the "
                        "Authority can be poisoned by whatever poisoned the join")

    ep8_commitment = (source_artifact.get("c2AuthorityJoin") or {}).get(
        "expectedPlanIntentCommitment")
    join = contract.get("c2AuthorityJoin") or {}
    if join.get("expectedPlanIntentCommitment") != ep8_commitment:
        findings.append("EP12-COMMITMENT-MOVED: c2AuthorityJoin."
                        "expectedPlanIntentCommitment differs from the digest-pinned "
                        "EP8 artifact's value")
    if join.get("expectedPlanIntentCommitment") not in \
            heavy["delegate"]["stability"]["distinctCommitments"]:
        findings.append("EP12-COMMITMENT-MOVED: the declared commitment is not a "
                        "member of the set this run recomputed through C-2 v4")

    if (contract.get("checkerModeContract") or {}).get(
            "exitMatrixIsObservedBehaviourally") is not True:
        findings.append("EP12-EXIT: checkerModeContract must declare the exit "
                        "matrix observed behaviourally")

    counterparts = authority.cache.get("counterparts")
    if counterparts is None:
        counterparts = {}
        authority.cache["counterparts"] = counterparts
    counterparts["c2-route"] = heavy["answerProvenance"]
    counterparts["route-introspection"] = {
        "rebound": heavy["rebound"],
        "installationDefectsAfterDrive": heavy["installationDefectsAfterDrive"],
        "anchorsUnmoved": heavy["answerProvenance"].get("anchorsUnmoved"),
        "executed": True}
    counterparts["non-circularity"] = heavy["delegate"]["stability"]
    if not _NESTED[0]:
        matrix = exit_matrix_probe(contract, HERE / BINDING, authority, snapshots,
                                   full=False)
        counterparts["selftest-dispatch"] = matrix
        for item in matrix:
            if not item["agrees"]:
                findings.append(f"EP12-EXIT: invocation {item['invocation']!r} "
                                f"returned {item['observed']}, expected "
                                f"{item['expected']}")
        counterparts["integer-guard"] = "EXECUTING"
        battery = own_constant_leaf_battery(contract, authority, snapshots)
        counterparts["integer-guard"] = battery
        published_battery = (contract.get("astScanScope") or {}).get(
            "ownConstantLeafBattery") or {}
        for key in ("intBoolLeaves", "cases", "rejected", "silentlyAdmitted",
                    "silentlyAdmittedPositions"):
            _expect(published_battery, key, battery[key],
                    "EP12-BATTERY: ownConstantLeafBattery", findings)

    root_census, _paths = node_census(contract)
    findings += verify_scans(contract, heavy, counterparts)
    findings += verify_totality(contract, heavy, root_census)

    authority.measurement = {**heavy, "contractRoot": root_census,
                             "counterparts": counterparts}
    return findings


# --------------------------------------------------------------------------
# Section 12.  Selftest and entrypoint.
#
# IR-EP11-NB-04: two of the predecessor's thirty-six mutations targeted paths
# that do not exist in its candidate, so assigning a NEW key raised nothing and
# the rows silently became a different test — one of them was rejected only by
# census arithmetic and exercised nothing about the thing it named.  Two repairs
# here, and both matter for the reason IMPLEMENTATION-FREEZE 7 records: a
# non-zero exit is not evidence that your guard fired.
#   1. every mutation path is RESOLVED in the base candidate before the suite
#      runs, and a path that does not resolve is a suite defect, not a pass; and
#   2. every mutation declares the finding id prefix that must reject it, and a
#      row rejected by some OTHER rule is reported as MIS-CAUGHT rather than
#      counted as a success.
# --------------------------------------------------------------------------

SELFTEST_MUTATIONS = (
    ("version is the JSON float 12.0", ("version",), 12.0, "EP12-TYPE"),
    ("version is JSON true", ("version",), True, "EP12-TYPE"),
    ("status silently applied", ("status",), "APPLIED", "EP12-POSTURE"),
    ("reviewState pre-cleared", ("reviewState",), "REVIEWED", "EP12-POSTURE"),
    ("sealRecommendation flipped", ("sealRecommendation",), "SEAL",
     "EP12-POSTURE"),
    ("assurance state escalated", ("assurance", "state"), "QUALIFIED",
     "EP12-POSTURE"),
    ("evidence grade escalated", ("assurance", "evidenceGrade"), "EXECUTED",
     "EP12-POSTURE"),
    ("RET-EP12-01 softened into a scoping note",
     ("retractions", 0, "disposition"), "SCOPED", "EP12-RETRACT"),
    ("RET-EP12-01 retracted text detached from its subject",
     ("retractions", 0, "retractedText"),
     "a fragment that does not occur in the pinned predecessor at all, of "
     "amply sufficient length to pass a bare minimum-length test", "EP12-RETRACT"),
    ("RET-EP12-01 retracted text reduced to one character",
     ("retractions", 0, "retractedText"), "a", "EP12-RETRACT"),
    ("a retraction pointed at a different string in the same subject",
     ("retractions", 0, "subjectPath"), "$.artifact", "EP12-RETRACT"),
    ("a retraction pointed at an OBJECT rather than at the claim",
     ("retractions", 0, "subjectPath"), "$.answerProvenance", "EP12-RETRACT"),
    ("answer provenance demoted to call provenance",
     ("answerProvenance", "establishesCallProvenanceOnly"), True, "EP12-ANSWER"),
    ("the anchor conceded to be the seat after all",
     ("answerProvenance", "anchoredToTheSeat"), True, "EP12-ANSWER"),
    ("the sole-guard disclosure withdrawn",
     ("answerProvenance", "isSoleGuardForAnswerProvenance"), False, "EP12-ANSWER"),
    ("a sentinel-flow count overstated",
     ("answerProvenance", "repairedSentinelFlowed"), 99, "EP12-ANSWER"),
    ("the anchored-object count understated",
     ("answerProvenance", "anchoredObjectAgreements"), 0, "EP12-ANSWER"),
    ("the installation-integrity count flattered",
     ("answerProvenance", "installationIntact"), 99, "EP12-ANSWER"),
    ("the unanchored-agreement count flattered",
     ("answerProvenance", "unanchoredValueAgreements"), 99, "EP12-ANSWER"),
    ("the anchor-integrity flag flipped",
     ("answerProvenance", "anchorsUnmoved"), False, "EP12-ANSWER"),
    ("the scope statement quietly softened",
     ("answerProvenance", "scopeStatement"),
     "This property is established against a hostile ROUTE REGION.",
     "EP12-ANSWER"),
    ("the anchor statement reduced to a slogan",
     ("answerProvenance", "anchorStatement"),
     "the anchor is the function object the verified bytes defined.",
     "EP12-ANSWER"),
    ("the seat-substitution control's A-6 result flattered",
     ("answerProvenance", "positiveControl", "seatSubstitution",
      "installationIntact"), 7, "EP12-ANSWER"),
    ("the predecessor-defeat control denied",
     ("predecessorDefeatControl", "predecessorIsDefeated"), False,
     "EP12-PREDECESSOR"),
    ("the predecessor-defeat seat attribution emptied",
     ("predecessorDefeatControl", "verdictsUnderTheVariantBy"), {},
     "EP12-PREDECESSOR"),
    ("call provenance claimed sufficient alone",
     ("callProvenance", "isSufficientAlone"), True, "EP12-CALL"),
    ("the call-ledger limitation deleted",
     ("callProvenance", "whatThisDoesNotEstablish"), "nothing further",
     "EP12-CALL"),
    ("the guard inventory claims total coverage",
     ("guardInventory", "claimsTotalCoverage"), True, "EP12-INVENTORY"),
    ("a sole guard's disclosure withdrawn from the inventory",
     ("guardInventory", "soleGuardVariants"), [], "EP12-INVENTORY"),
    ("the inventory's completeness statement rewritten",
     ("guardInventory", "why"), "Every guard is listed here.", "EP12-INVENTORY"),
    ("an unscored guard given a sole-guard boolean nothing measured",
     ("guardInventory", "guards", 5, "isSoleGuardForSomeClass"), False,
     "EP12-INVENTORY"),
    ("the differential oracle claimed sufficient alone",
     ("differentialOracle", "isSufficientAlone"), True, "EP12-DIFF"),
    ("the per-variant evasion matrix edited",
     ("evasionMeasurement", "perVariant"), [], "EP12-EVASION"),
    ("the declared escapes hidden",
     ("evasionMeasurement", "escapedEveryGuard"), [], "EP12-EVASION"),
    ("the tripwire's measured blindness deleted",
     ("evasionMeasurement", "tripwireOutcome"), [], "EP12-EVASION"),
    ("the escape set reclaimed as a coverage claim",
     ("evasionMeasurement", "escapeSetIsAMeasurementNotACoverageClaim"), False,
     "EP12-EVASION"),
    ("a preserved regime-B admitted set deleted",
     ("preservedMeasurements", "regimes", "B", "admitted"), [], "EP12-PRESERVED"),
    ("preserved identity movement beneath an identical seal denied",
     ("preservedMeasurements", "identityMovingUnderByteIdenticalSeal"), 0,
     "EP12-PRESERVED"),
    ("the plan-intent silent-accept enumeration reduced to a count",
     ("scalarLeafTotality", "surfaces", 0, "silentAcceptPositions"), [],
     "EP12-TOTALITY"),
    ("the plan-descriptor silent-accept enumeration emptied",
     ("scalarLeafTotality", "surfaces", 1, "silentAcceptPositions"), [],
     "EP12-TOTALITY"),
    ("contract-root census understated",
     ("scalarLeafTotality", "contractRoot", "scalarLeafPaths"), 1,
     "EP12-TOTALITY"),
    ("the injection-isolation measurement fabricated",
     ("scalarLeafTotality", "injectionIsolation", "sharedValuesMutated"),
     ["json-empty-object"], "EP12-TOTALITY"),
    ("a pinned digest edited",
     ("delegationClosure", "executables", 0, "sha256"), "0" * 64, "EP12-RECORD"),
    ("the pin-agreement scope claim widened",
     ("delegationClosure", "pinAgreementRule"),
     "every predecessor's own declared pin table is cross-checked",
     "EP12-CLOSURE"),
    ("the RES-EP12-01 residual deleted",
     ("c2AuthorityRepairJoin", "ep6InnerJoinResidual"), "closed", "EP12-RESIDUAL"),
    ("RES-EP12-02 hollowed to length with every anchor intact",
     ("knownLimitations", 1, "text"),
     "RES-EP12-02. The ROUTE REGION is the declared hostile surface of this "
     "instrument and everything about it is well understood. A mutation that "
     "reaches this guard's own stack frame is NOT closed and never could be by "
     "anything running in the same process, which is a general truth about "
     "software rather than a fact about this run. AX6 is a name for that class "
     "and RX2c is another name for it. The source tripwire is an enumeration and "
     "an enumeration has the properties that enumerations have. There is nothing "
     "further of substance to say here, and this paragraph is long enough to "
     "satisfy any minimum-length test that a checker might reasonably impose on "
     "the disclosure of a residual risk of this kind.", "EP12-RESIDUAL"),
    ("RES-EP12-02's bound measurement edited to something comfortable",
     ("knownLimitations", 1, "boundValueText"), "no variant escaped every guard",
     "EP12-RESIDUAL"),
    ("a text-only residual dressed up as a measured binding",
     ("knownLimitations", 10, "enforcement"), "MEASURED-BINDING", "EP12-RESIDUAL"),
    ("RES-EP12-13 hollowed of the measurement it restates",
     ("knownLimitations", 12, "text"),
     "RES-EP12-13. The predecessor's injection helper is order-dependent because "
     "it shares mutable table members, and this instrument deep-copies. It is "
     "worth saying that no guard mutated anything and that the earlier review had "
     "nothing to catch, which is a pleasant thing to be able to record and costs "
     "nothing to write down here at whatever length a minimum-length rule happens "
     "to require of a residual that is, in the end, about a hazard that has never "
     "had an instance anywhere in this corpus at all.", "EP12-RESIDUAL"),
    ("the residual-enforcement accounting flattered",
     ("knownLimitationsEnforcement", "boundToAMeasurement"), 17, "EP12-RESIDUAL"),
    ("the non-circularity measurement understated",
     ("astScanScope", "nonCircularity", "uniqueHexLiterals"), 1, "EP12-SCAN"),
    ("a source scan reclaimed as free of blind spots",
     ("astScanScope", "routingScanCannotSeeWhoseAnswerIsUsed"), False, "EP12-SCAN"),
    ("the enumeration reinstated as the support for a published property",
     ("astScanScope", "noPublishedPropertyRestsOnAnEnumeration"), False,
     "EP12-SCAN"),
    ("the introspection enumeration's measured size edited",
     ("astScanScope", "introspectionEnumeratedSpellings"), 1, "EP12-SCAN"),
)


def _resolve_mutation_path(contract, mutation_path):
    cursor = contract
    for key in mutation_path[:-1]:
        cursor = cursor[key]
    final = mutation_path[-1]
    if isinstance(cursor, dict):
        if final not in cursor:
            raise KeyError(final)
    else:
        cursor[final]  # noqa: B018 - raises IndexError if the index is absent
    return cursor


def selftest(contract, authority, path, snapshots) -> int:
    base = check(contract, authority, snapshots)
    if base:
        print("SELFTEST-REFUSED: the base candidate is already dirty; a mutation "
              "suite over a dirty base proves nothing")
        for item in base[:5]:
            print("  -", item)
        print(f"SELFTEST-NOT-RUN: 0 of {len(SELFTEST_MUTATIONS)} mutations executed")
        return 3

    print(f"EP12 SELFTEST — {path.name}")
    print()
    unresolved = []
    for label, mutation_path, _injected, _prefix in SELFTEST_MUTATIONS:
        try:
            _resolve_mutation_path(contract, mutation_path)
        except MALFORMED:
            unresolved.append(f"{label}: {list(mutation_path)} does not resolve")
    if unresolved:
        for item in unresolved:
            print("SELFTEST-DEFECT:", item)
        print(f"SELFTEST-NOT-RUN: {len(unresolved)} mutation(s) target a path that "
              "does not exist in the base candidate; a mutation that cannot "
              "perturb what it names reports coverage it does not have")
        return 1

    escaped: list[str] = []
    for label, mutation_path, injected, prefix in SELFTEST_MUTATIONS:
        mutated = copy.deepcopy(contract)
        cursor = mutated
        for key in mutation_path[:-1]:
            cursor = cursor[key]
        cursor[mutation_path[-1]] = injected
        _NESTED[0] += 1
        try:
            findings = check(mutated, authority, snapshots)
        finally:
            _NESTED[0] -= 1
        matched = [item for item in findings if item.startswith(prefix)]
        if matched:
            print(f"  reject  {label}")
            print(f"            -> {matched[0][:140]}")
        elif findings:
            escaped.append(f"{label}: MIS-CAUGHT — rejected by {findings[0][:60]!r} "
                           f"and not by {prefix}")
            print(f"  MISCAUGHT {label}: no {prefix} finding")
        else:
            escaped.append(label)
            print(f"  ESCAPE  {label}")

    print()
    matrix = exit_matrix_probe(contract, path, authority, snapshots, full=True)
    print("  exit matrix, observed BEHAVIOURALLY by driving main() in-process:")
    for item in matrix:
        verdict = "ok " if item["agrees"] else "BAD"
        print(f"    {verdict} {item['invocation']}: expected {item['expected']}, "
              f"observed {item['observed']} ({item['outputLines']} output lines)")
        if not item["agrees"]:
            escaped.append(f"exit matrix: {item['invocation']}")

    measurement = authority.measurement
    evasion = measurement["evasion"]
    print()
    print("  evasion battery, re-stated from this run (guard columns in order "
          f"{list(GUARD_IDS)}; T = flagged by the unscored introspection "
          "tripwire):")
    tripwire = {item["variant"]: item["flagged"]
                for item in evasion["tripwireOutcome"]}
    for item in evasion["perVariant"]:
        flags = "".join("Y" if item.get(key) else "." for key in GUARD_IDS)
        mark = "T" if tripwire.get(item["variant"]) else "-"
        print(f"    {flags} {mark}  {item['variant']}")
    print(f"  variants that escaped every SCORED guard: "
          f"{evasion['escapedEveryGuard'] or 'none'}")
    print(f"  declared in advance to escape: {list(DECLARED_ESCAPES)} — this is a "
          "MEASUREMENT over the classes built here, not a coverage claim")
    battery = (measurement.get("counterparts") or {}).get("integer-guard") or {}
    print(f"  own constant-leaf battery: {battery.get('intBoolLeaves')} int/bool "
          f"leaves, {battery.get('cases')} cases, {battery.get('rejected')} "
          f"rejected, {battery.get('silentlyAdmitted')} silently admitted")
    predecessor = measurement["predecessor"]
    print(f"  predecessor-defeat control: {EP11} answer-provenance findings for "
          f"{predecessor.get('variant')} = "
          f"{predecessor.get('predecessorAnswerProvenanceFindings')}; verdict "
          f"attribution under the variant {predecessor.get('verdictsUnderTheVariantBy')}, "
          f"unmodified {predecessor.get('verdictsUnderTheUnmodifiedPredecessorBy')}; "
          f"this instrument's findings for the same variant = "
          f"{predecessor.get('thisInstrumentAnswerProvenanceFindings')}")

    print()
    if escaped:
        for item in escaped:
            print("SELFTEST-FAIL:", item)
        print(f"{len(escaped)} retained case(s) ESCAPED or were MIS-CAUGHT — the "
              "proof path is optional")
        return 1
    print(f"SELFTEST-PASS: all {len(SELFTEST_MUTATIONS)} mutations rejected BY THE "
          "RULE EACH ONE NAMES, every mutation path resolved in the base candidate, "
          "and the 0/1/2/3 exit matrix agrees behaviourally")
    print("  RES-EP12-01: v12 does NOT repair check-evaluation-proof-v6.py; EP6's "
          "inner C-2 join still runs against the DEFECTIVE check-c2.py bytes")
    print("  RES-EP12-02: a route region that reads or writes this guard's own "
          "stack frame is NOT closed by this instrument; AX6, AX9 and RX2c are "
          "built, executed and published as measured escapes")
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
        print(f"EP12-UNSUPPORTED-INVOCATION: {exc}", file=sys.stderr)
        return 2
    try:
        if override and override.get("authority") is not None:
            authority = override["authority"]
            snapshots = override["snapshots"]
        else:
            snapshots = load_snapshots()
            authority = build_authority(snapshots)
    except AuthorityLoadError as exc:
        print(f"EP12-PINNED-INPUT-REFUSED: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2
    path = pathlib.Path(requested) if requested is not None else HERE / BINDING
    try:
        text = override["candidateText"] if override and "candidateText" in override \
            else path.read_text()
        contract = json.loads(text, object_pairs_hook=_pairs)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        print(f"cannot load the EP12 candidate {path}: {type(exc).__name__}: {exc}",
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
    predecessor = measurement["predecessor"]
    root = measurement["contractRoot"]
    descriptor = measurement["descriptorSurface"]
    isolation = measurement["isolation"]
    regime_a, regime_b = delegate_heavy["regimeA"], delegate_heavy["regimeB"]
    moving = [item for item in regime_b["admitted"]
              if item["classification"] == "type-distinct-one" and
              item["movedIdentities"]]
    under_seal = [item for item in moving
                  if "evaluationAuthoritySealRef" not in item["movedIdentities"]]
    bound = len(RESIDUAL_BINDINGS) - len(TEXT_ONLY_RESIDUALS)

    print(f"EP12 contract OK — {path.name}")
    print(f"  delegation closure: {len(DELEGATED_CHECKER)} delegated checker + "
          f"{len(PREDECESSOR_INSTRUMENT)} pinned predecessor instrument + "
          f"{len(DELEGATION_CLOSURE)} executables + {len(PINNED_DATA)} pinned data "
          "inputs + 1 superseded independent encoder, each read ONCE, SHA-256 "
          "verified, then executed or parsed from that verified byte string; every "
          "one recorded by filename and digest")
    print(f"  C-2 join RE-PINNED onto {C2V4_CONTRACT} / {C2V4}")
    print(f"  ANSWER PROVENANCE ESTABLISHED, WITHIN THE SCOPE PRINTED ON THE NEXT "
          f"TWO LINES, for {answer['vectors']} pinned vectors x "
          f"{answer['apisPerVector']} imported APIs = "
          f"{answer['expectedPerRuleTotal']} answers: "
          f"{answer['independentValueAgreements']} equal the value an INDEPENDENT "
          f"instance of {C2V4} computed (A-1); "
          f"{answer['anchoredObjectAgreements']} ARE the object produced by the "
          "function object the SHA-256-verified bytes defined, compared by `is` "
          "against this guard's own frame-local anchor (A-2); "
          f"{answer['repairedSentinelFlowed']} FOLLOW a sentinel injected into "
          "every reachable spelling of the repaired api (A-3); "
          f"{answer['supersededSentinelIgnored']} are UNMOVED by the same "
          f"injection into the superseded module (A-4); {answer['gateAgreements']} "
          f"accept/reject gates agree (A-5); {answer['installationIntact']} vectors "
          "found the load-time installation still identical before, during and "
          f"after the drive (A-6); {answer['unanchoredValueAgreements']} answers "
          "agree with the reference instance when this guard installs NOTHING "
          f"(A-7); anchors unmoved {answer['anchorsUnmoved']}, record parity held "
          f"for {answer['recordParityHeld']} vectors (A-8)")
    print("  SCOPE OF THAT LINE, printed here and not only in the residuals: it "
          "holds against a hostile ROUTE REGION. It does NOT hold against a route "
          "region that reads or writes this guard's own stack frame or the closure "
          f"cells of the servers it installs — {list(DECLARED_ESCAPES)} do exactly "
          "that, are built and executed on this run, and are MEASURED to defeat "
          "every scored guard")
    print("  SCOPE, second half: the source tripwire that flags the cheap spellings "
          "of that class is an ENUMERATION of "
          f"{route_introspection_scan()['enumeratedSpellings']} identifiers, it is "
          "NOT a scored guard, and RX2c is measured on this run to escape it. No "
          "property printed above rests on it")
    print(f"  PREDECESSOR DEFEATED, MEASURED, NOT ASSERTED: the blocking evasion "
          f"{predecessor['variant']} rebuilt inside {EP11}'s own route region "
          f"produces {predecessor['predecessorAnswerProvenanceFindings']} "
          "answer-provenance finding(s) there with every rule at full agreement, "
          "and the pinned verdicts it serves are attributed "
          f"{predecessor['verdictsUnderTheVariantBy']} against "
          f"{predecessor['verdictsUnderTheUnmodifiedPredecessorBy']} for the "
          "unmodified predecessor in the identical harness. The same region here "
          f"produces {predecessor['thisInstrumentAnswerProvenanceFindings']} "
          "finding(s)")
    print(f"  CALL PROVENANCE, and no more than that: {call['observedCalls']} C-2 "
          f"calls observed per call across {call['vectorsDriven']} vectors, "
          f"{call['distinctFingerprintsObserved']} distinct PlanIntent "
          f"fingerprint(s), {call['supersededCallsInsideJoin']} served by the "
          "superseded module. This establishes WHICH MODULE WAS CALLED, not whose "
          "answer was used")
    print(f"  positive control on the guard: the decoy-call join produces "
          f"{control['decoyCall']['findingCount']} answer-provenance finding(s) "
          f"while A-1 still agrees "
          f"{control['decoyCall']['independentValueAgreements']}/"
          f"{answer['expectedPerRuleTotal']} times; the forged-ledger join has the "
          f"SHARED ledger agreeing "
          f"{control['forgedLedgerEntry']['sharedLedgerAgreements']} times and the "
          f"anchored witness agreeing "
          f"{control['forgedLedgerEntry']['anchoredObjectAgreements']} times; the "
          "seat-substitution join leaves the load-time installation intact for "
          f"{control['seatSubstitution']['installationIntact']} of "
          f"{answer['vectors']} vectors")
    print(f"  evasion battery: {evasion['variantsBuilt']} variants BUILT AND "
          f"EXECUTED ({evasion['sourceVariantsBuilt']} route-region rewrites + "
          f"{evasion['objectAttacksBuilt']} object attacks); per-guard catches "
          f"{evasion['perGuardCatchCount']}; caught by at least one scored guard "
          f"{evasion['caughtByAtLeastOneGuard']}; ESCAPED EVERY SCORED GUARD "
          f"{evasion['escapedEveryGuard'] or '[]'} — DECLARED IN ADVANCE and "
          "MEASURED over the classes built here, which is not a coverage claim "
          "over the space of evasions; answer-provenance is the SOLE catcher of "
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
    print(f"  differential oracle (RETAINED, NOT SUFFICIENT ALONE, computed on a "
          f"PRIVATE instance): {oracle['stats']['executedCases']} executed cases, "
          f"{oracle['stats']['joinVsRepairedMismatches']} join-vs-repaired "
          f"mismatches, discriminating cardinality "
          f"{oracle['discriminatingCardinality']}; injection isolation measured "
          f"over {isolation['casesDriven']} injections through "
          f"{isolation['guardsDriven']} guards -> table members mutated "
          f"{isolation['sharedValuesMutated']}")
    print("  silent accepts ENUMERATED, not counted (IR-EP10-NB-03): plan-intent "
          f"{len(oracle['silentAcceptPositions'])} position(s), plan-descriptor "
          f"{len(descriptor['silentAcceptPositions'])} position(s), each published "
          "in full and required to match exactly")
    print(f"  residual enforcement: {bound} of {len(RESIDUAL_BINDINGS)} residuals "
          "are bound to a value THIS RUN recomputes and must quote verbatim; "
          f"{len(TEXT_ONLY_RESIDUALS)} — {list(TEXT_ONLY_RESIDUALS)} — have no "
          "in-process measurement and are declared TEXT-ONLY rather than given a "
          "test that would pass on hollow text")
    print(f"  contract-root space measured at {root['enumeratedPaths']} paths of "
          f"which {root['scalarLeafPaths']} are scalar leaves")
    print("  RES-EP12-01: v12 does NOT repair check-evaluation-proof-v6.py; EP6's "
          "inner C-2 join still runs against the DEFECTIVE check-c2.py bytes "
          "underneath EP8, and v12 is a strictly stronger OUTER gate over it")
    print("  RES-EP12-15: check-c2-v4.py's own published self-census is under a "
          "BLOCKING adjudication (IR-C2V4-01) today. v12 pins v4's bytes and does "
          "not chase a moving target onto v5; the defect is in v4's measurement of "
          "its own counters, not in the admission API this join depends on")
    print("  RES-EP12-09: provenance is not correctness. These rules establish that "
          f"the answer used is {C2V4}'s answer, not that {C2V4} is right")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED / "
          "AWAITING-INDEPENDENT-REVIEW; DO-NOT-SEAL; CD-RT-5 unsigned and "
          "BLOCKED_ON_PHASE_1A; independent re-review REQUIRED")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
