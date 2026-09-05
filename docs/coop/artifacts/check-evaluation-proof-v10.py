#!/usr/bin/env python3
"""check-evaluation-proof-v10.py — executable checker for evaluation-proof.v10.json.

v10 is the successor to evaluation-proof.v9.json, which an independent reviewer
REJECTED (ep9.review-independent.json, 2 blocking findings).  v10 exists to
repair those two findings BY MEASUREMENT and to retract what v9 published
falsely.  Every number in the banner is recomputed from the live bytes on this
run and compared against the candidate; nothing is transcribed from v9.

============================================================================
WHAT v10 DOES *NOT* CLAIM — read this before reading the green banner
============================================================================
RES-EP10-01  v10 does NOT repair check-evaluation-proof-v6.py.  EP6 is pinned by
             passed work and out of scope for edit.  EP6's INNER C-2 join still
             executes against the DEFECTIVE check-c2.py bytes underneath EP8.
             v10, like v9, is a strictly stronger OUTER gate over that join, not
             a replacement of its internals.  Closing the inner join requires a
             v6 successor and is NOT closed here.

RET-EP10-01  v9's RES-EP9-05 stated that the `!= 1` type-level false-accept class
             "moves NO proof identity ... because every ref is derived from the
             stored raw CAS bytes rather than from the in-memory record".
             THAT IS FALSE AND IS RETRACTED OUTRIGHT — not softened, not
             rescoped.  check-evaluation-proof-v8.py computes
             `admission_ref = ep6.raw_record_ref("EvaluationAuthorityAdmissionV1",
             admission)` from the IN-MEMORY candidate record, and that value is
             written into the durable EvaluationAuthorityIndexV1 row and into the
             index fingerprint.  Under producer consistency the class DOES MOVE
             DURABLE IDENTITY, and it does so beneath a BYTE-IDENTICAL
             EvaluationAuthoritySealRef — strictly WORSE than a visible mismatch,
             because two byte-distinct raw lineages then resolve under one and
             the same seal ref and the store cold-reconstructs either of them
             with assert_store_continuity() returning True.  v10 MEASURES this.

RET-EP10-02  v9's "exact admitted set" is retracted.  A regime that injects at
             ONE in-memory position while leaving the stored CAS bytes at their
             honest encoding is structurally incapable of observing identity
             movement, because the refs are then re-derived from bytes the
             injection never touched.  v10 re-derives the admitted set BY
             EXECUTION under TWO declared encoder regimes and publishes which
             regime each position was measured under.

RET-EP10-03  v9's astScanScope named "the LB-C2-01 behavioural battery and the
             Authority.c2v4 access counter" as the load-bearing guard for the C-2
             routing property.  Both are insufficient and both are retracted as
             guards: the battery's entire discriminating power is a FIXED 8-case
             family, so it is teachable by whitelist; and the counter counts
             accessor TOUCHES, not which module SERVED the call.  v10 replaces
             them with a per-call served-module ledger bound to the specific
             pinned vectors, and MEASURES that a differential oracle — the
             alternative the reviewer named — does not catch the R1/R4 class.

RET-EP10-04  v9's headline "7 vectors ... distinct commitments [1]" is retracted
             as an overstatement.  All seven positiveVectors carry ONE distinct
             frozenPlanIntent and ONE distinct planDescriptor; a distinct-
             commitment count of 1 is FORCED BY THE INPUT and establishes
             nothing about the encoder.  v10 publishes the measured distinct-
             intent count beside it and adds a separately labelled family of
             legally distinct PlanIntents that does carry discriminating power.

RES-EP10-02  The AST scans here are TRIPWIRES.  Every property a scan guards is
             listed in astScanScope with the INDEPENDENT BEHAVIOURAL LAYER that
             guards it; every counterpart is EXECUTED on every ordinary run; and
             the set of properties for which a scan is the sole guard is MEASURED
             and required to be empty.

RES-EP10-03  Reported honestly and NOT used to downgrade anything: the reviewer's
             2548-case differential fuzz of check-c2.py against check-c2-v4.py
             over the corpus's only distinct PlanIntent found divergence at
             exactly the 4 LB-C2-01 (path,value) pairs.  So a routing evasion
             produces no wrong ANSWER on today's pinned bytes.  The defect the
             served-module ledger closes is in the EVIDENCE, not currently in the
             verdict.  That is a reason to measure routing behaviourally, not a
             reason to treat it as minor.

RES-EP10-04  Checker-scope evidence only: guarded in-memory test doubles.  No
             production store, durable backend, host admission or transaction
             implementation is demonstrated.

Usage:
    python3 -I -B check-evaluation-proof-v10.py [artifact.json]
    python3 -I -B check-evaluation-proof-v10.py --selftest

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
import sys
import types
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
BINDING = "evaluation-proof.v10.json"
EXPECTED_VERSION = 10
DECLARED_FLAGS = ("--selftest",)

MALFORMED = (TypeError, ValueError, KeyError, IndexError, AttributeError,
             ZeroDivisionError, OverflowError, RecursionError, UnicodeError,
             StopIteration)

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
EP9_ARTIFACT = "evaluation-proof.v9.json"
EP9_REVIEW = "ep9.review-independent.json"
EP8_ARTIFACT = "evaluation-proof.v8.json"

# --------------------------------------------------------------------------
# Recording obligation, IMPLEMENTATION-FREEZE 7.2: every input this verdict
# depends on is recorded by FILENAME AND SHA-256.  A count is not a record and a
# prose assertion is not a record.
# --------------------------------------------------------------------------

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

ALL_PINS = {**DELEGATION_CLOSURE, **SUPERSEDED_ENCODER, **PINNED_DATA}

C2_IMPORTED_APIS = ("validate_plan_intent", "plan_intent_commitment",
                    "canonical_plan_intent")

# The vector source is evaluation-proof.v8.json, which carries a PASSING
# independent review.  evaluation-proof.v9.json is REJECTED, so v10 takes no
# vector authority from it; it is pinned, parsed and required to AGREE.
VECTOR_SOURCE = EP8_ARTIFACT

# Re-entrancy depth for the in-process behavioural probes.  A nested run never
# re-runs the counterparts, so the probes terminate.
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


# --------------------------------------------------------------------------
# Section 0.  Trust order.
#
# Every transitive input is read ONCE as inert bytes, SHA-256 verified against
# the pin table above, and thereafter executed or parsed EXCLUSIVELY from that
# verified in-memory byte string.  There is no second disk read between
# verification and execution for anything v10 loads.
#
# Stated so the rule is not over-read: the PREDECESSORS re-read some of their
# own pinned data from disk while executing (EP6.admit_evaluation_authority
# re-reads c2-plan-stage-schema.v3.json and fact-plane.v1.json on every call;
# EP8._ep7 sha_file()-verifies and then loads from disk).  Both hash-verify what
# they re-read, so the trust order holds transitively, but the guarantee v10
# makes is about what v10 loads.
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


def _exec_verified(filename: str, source: bytes):
    _MODULE_SERIAL[0] += 1
    name = f"_ep10_{_MODULE_SERIAL[0]}_{re.sub(r'[^0-9a-zA-Z]', '_', filename)}"
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


# --------------------------------------------------------------------------
# Section 1.  The served-module ledger — THE load-bearing routing guard.
#
# It reads NO source.  Both C-2 module objects are instrumented once, at load
# time: each of the three imported APIs is rebound ON THE MODULE OBJECT to a
# wrapper that records, PER CALL, which module actually served it, at what
# nesting depth, over which argument fingerprint, and which result object it
# produced.  The tag is fixed at install time from the module the wrapper was
# installed on, so no caller can influence it and no spelling of the call can
# avoid it.
#
# Why this and not v9's counter (RET-EP10-03): a counter records THAT a call
# happened.  It counts accessor TOUCHES.  The reviewer's R4 evasion touches the
# accessor on every path and still routes 100% of the real vectors to the
# superseded module, so the counter stays green.  This ledger records WHICH
# MODULE SERVED WHICH ARGUMENT, so the guard can require that the answer used
# for each SPECIFIC pinned vector came out of the repaired module.
# --------------------------------------------------------------------------

class ServedCall:
    __slots__ = ("seq", "tag", "api", "depth", "argfp", "label", "result")

    def __init__(self, seq, tag, api, depth, argfp, label):
        self.seq = seq
        self.tag = tag
        self.api = api
        self.depth = depth
        self.argfp = argfp
        self.label = label
        self.result = None


class LedgerWindow:
    __slots__ = ("ledger", "label", "start", "stop")

    def __init__(self, ledger, label):
        self.ledger = ledger
        self.label = label
        self.start = len(ledger.entries)
        self.stop = None

    @property
    def entries(self):
        stop = len(self.ledger.entries) if self.stop is None else self.stop
        return self.ledger.entries[self.start:stop]


class ServedLedger:
    def __init__(self):
        self.entries: list[ServedCall] = []
        self.installed: dict[str, int] = {}
        self.originals: dict[tuple[str, str], Any] = {}
        self._depth = 0
        self._labels: list[str] = []
        self._provenance: dict[int, str] = {}
        self._ambiguous: set[int] = set()

    def install(self, module, tag: str) -> None:
        if tag in self.installed:
            raise AuthorityLoadError(f"ledger already installed for {tag}")
        for api in C2_IMPORTED_APIS:
            original = getattr(module, api, None)
            if original is None or not callable(original):
                raise AuthorityLoadError(f"{tag} does not expose a callable {api}")
            self.originals[(tag, api)] = original
            setattr(module, api, self._wrap(original, api, tag))
        self.installed[tag] = id(module)

    def _wrap(self, original, api: str, tag: str):
        ledger = self

        def served(*args, **kwargs):
            label = ledger._labels[-1] if ledger._labels else None
            entry = ServedCall(len(ledger.entries), tag, api, ledger._depth,
                               value_fingerprint(args[0]) if args else None, label)
            ledger.entries.append(entry)
            ledger._depth += 1
            try:
                result = original(*args, **kwargs)
            finally:
                ledger._depth -= 1
            entry.result = result
            key = id(result)
            if key in ledger._provenance and ledger._provenance[key] != tag:
                ledger._ambiguous.add(key)
            ledger._provenance[key] = tag
            return result

        served.__ledger_tag__ = tag
        served.__ledger_api__ = api
        return served

    @contextlib.contextmanager
    def window(self, label: str):
        handle = LedgerWindow(self, label)
        self._labels.append(label)
        try:
            yield handle
        finally:
            self._labels.pop()
            handle.stop = len(self.entries)

    def provenance(self, result) -> str | None:
        key = id(result)
        if key in self._ambiguous:
            return "AMBIGUOUS"
        return self._provenance.get(key)


# --------------------------------------------------------------------------
# Section 2.  The Authority: everything admitted after hash verification.
# --------------------------------------------------------------------------

class Authority:
    def __init__(self, snapshots, parsed, modules, ledger):
        self.snapshots = snapshots
        self.parsed = parsed
        self.modules = modules
        self.ledger = ledger
        # RETAINED BUT DEMOTED (RET-EP10-03): a liveness aid, NOT the guard.
        self.c2v4_accesses = 0
        self.measurement: dict[str, Any] = {}
        self.cache: dict[str, Any] = {}

    def json(self, name):
        return self.parsed.get(name)

    def module(self, name):
        return self.modules.get(name)

    def c2v4(self):
        """The declared route to the repaired C-2 instrument."""
        self.c2v4_accesses += 1
        return self.modules[C2V4]

    def c2v3(self):
        """The superseded encoder, admitted only as an independent cross-check."""
        return self.modules[C2V3]


def build_authority(snapshots: dict[str, bytes]) -> Authority:
    parsed: dict[str, Any] = {}
    for name in PINNED_DATA:
        try:
            parsed[name] = json.loads(snapshots[name].decode("utf-8"),
                                      object_pairs_hook=_pairs)
        except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
            raise AuthorityLoadError(
                f"pinned data {name} is not parseable JSON: "
                f"{type(exc).__name__}: {exc}") from exc
    modules: dict[str, Any] = {}
    for name in list(DELEGATION_CLOSURE) + list(SUPERSEDED_ENCODER):
        modules[name] = _exec_verified(name, snapshots[name])
    ledger = ServedLedger()
    ledger.install(modules[C2V4], C2V4)
    ledger.install(modules[C2V3], C2V3)
    return Authority(snapshots, parsed, modules, ledger)


def load_authority(directory: pathlib.Path = HERE) -> Authority:
    return build_authority(load_snapshots(directory))


# --------------------------------------------------------------------------
# Section 3.  The C-2 v4 authority join.
#
# Every C-2 call this checker makes FOR AUTHORITY is spelled inside the marked
# region below, and the evasion battery rewrites exactly that region.
# --------------------------------------------------------------------------

# ROUTE-REGION-BEGIN

def c2_validate_intent(intent, authority):
    """Total.  Returns a findings list; never raises for parsed JSON."""
    try:
        contract = authority.json(C2V4_CONTRACT)
        relations = authority.json(FACT_PLANE)["relationRegistry"]["relations"]
        return list(authority.c2v4().validate_plan_intent(
            intent, contract, set(relations)))
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
# from the call: they are the unguarded control side of a matrix, the cross-check
# against the superseded encoder, or the differential oracle.
C2_MEASUREMENT_CLOSURE = ("commitment_stability", "distinct_intent_family",
                          "lb_c2_01_probe_family", "superseded_cross_check",
                          "differential_oracle", "c2_api_surface")


def c2_join(intent, authority):
    """The complete v10 authority join over one PlanIntent."""
    findings = list(c2_validate_intent(intent, authority))
    if findings:
        return None, findings, None
    commitment, encode_errors = c2_commit_intent(intent, authority)
    if encode_errors:
        return None, encode_errors, None
    preimage, canonical_errors = c2_canonical_intent(intent, authority)
    if canonical_errors:
        return None, canonical_errors, None
    if not preimage:
        return None, [("C2I-04", "repaired C-2 canonical PlanIntent unexpectedly "
                                 "empty")], None
    return commitment, [], preimage


def c2_api_surface(authority) -> list[str]:
    findings: list[str] = []
    module = authority.c2v4()
    for name in C2_IMPORTED_APIS:
        function = getattr(module, name, None)
        if function is None or not callable(function):
            findings.append(f"EP10-C2-API: {C2V4} does not expose a callable {name}")
            continue
        original = authority.ledger.originals.get((C2V4, name), function)
        try:
            arity = original.__code__.co_argcount
        except AttributeError:
            findings.append(f"EP10-C2-API: {name} in {C2V4} is not a plain function")
            continue
        expected = 3 if name == "validate_plan_intent" else 2
        if arity != expected:
            findings.append(f"EP10-C2-API: {C2V4}.{name} takes {arity} positional "
                            f"parameters; the imported seam requires {expected}")
    return findings


# --------------------------------------------------------------------------
# Section 4.  The behavioural routing guard — REP-EP10-2.
#
# For EVERY named pinned vector the join is driven inside a ledger window, and
# the guard requires, from the ledger and from nothing else:
#   R-1  the window is NON-EMPTY.  A join that reaches C-2 by a route the ledger
#        cannot observe records zero calls and is reported.  This is what
#        defeats "delete the instrumentation" and "hand the join an unwrapped
#        module": a silent instrument fails closed.
#   R-2  EVERY call observed in the window was served by the REPAIRED module.
#        Not "at least one"; every one.
#   R-3  every observed depth-0 call carries the FINGERPRINT OF THIS VECTOR'S
#        PlanIntent.  This is what binds the count to the SPECIFIC vectors: a
#        counter that ticks over a probe family cannot satisfy it.
#   R-4  all three imported APIs are observed at depth 0 for this vector, so a
#        join that validates through the repaired module and commits through the
#        superseded one is reported.
#   R-5  the commitment VALUE the join returned has repaired-module provenance,
#        recorded against the identity of the returned object itself.
#   R-6  aggregate: the number of DISTINCT PlanIntent fingerprints observed
#        equals the number of vectors driven, and zero superseded-module calls
#        occurred inside any authority-join window.
# --------------------------------------------------------------------------

def routing_ledger_guard(named_intents, authority):
    findings: list[str] = []
    rows: list[dict[str, Any]] = []
    observed: set[str] = set()
    superseded_calls = 0
    total_calls = 0

    for vector_id, intent in named_intents:
        want = value_fingerprint(intent)
        with authority.ledger.window(f"authority-join:{vector_id}") as window:
            commitment, errors, _preimage = c2_join(intent, authority)
        entries = window.entries
        outer = [call for call in entries if call.depth == 0]
        tags = sorted({call.tag for call in entries})
        apis = sorted({call.api for call in outer})
        mismatched = [call for call in outer if call.argfp != want]
        provenance = authority.ledger.provenance(commitment) if commitment else None
        total_calls += len(entries)
        superseded_calls += sum(1 for call in entries if call.tag != C2V4)
        observed.update(call.argfp for call in outer if call.argfp)

        if not entries:
            findings.append(
                f"EP10-ROUTE: vector {vector_id} produced ZERO observed C-2 calls; "
                "the authority join reached a C-2 API by a route the served-module "
                "ledger cannot observe, or made no call at all")
        if tags and tags != [C2V4]:
            findings.append(
                f"EP10-ROUTE: vector {vector_id}'s authority join was served by "
                f"{tags}; the C-2 join is re-pinned onto {C2V4} and EVERY call for "
                "a pinned vector must be served by the repaired module")
        if mismatched:
            findings.append(
                f"EP10-ROUTE: vector {vector_id} observed {len(mismatched)} depth-0 "
                "C-2 call(s) over an argument that is NOT this vector's PlanIntent; "
                "the routing evidence is not bound to the pinned vectors")
        if entries and apis != sorted(C2_IMPORTED_APIS):
            findings.append(
                f"EP10-ROUTE: vector {vector_id} exercised depth-0 APIs {apis}; all "
                f"three of {sorted(C2_IMPORTED_APIS)} must be served for every "
                "pinned vector or the join is only partly re-pinned")
        if errors:
            findings.append(
                "EP10-STABILITY: the repaired C-2 instrument rejects pinned vector "
                f"{vector_id}: {errors[0]}")
        elif provenance != C2V4:
            findings.append(
                f"EP10-ROUTE: the commitment returned for vector {vector_id} has "
                f"provenance {provenance!r}, not {C2V4}; the VALUE the join used "
                "was not produced by the repaired module")
        rows.append({"vectorId": vector_id, "observedCalls": len(entries),
                     "depthZeroCalls": len(outer), "servedBy": tags, "apis": apis,
                     "argumentBound": not mismatched,
                     "commitmentProvenance": provenance})

    # RET-EP10-04 discipline applied to the guard itself: the aggregate rule
    # compares against the number of DISTINCT intents the vectors actually carry,
    # measured here, not against the vector COUNT.  The seven pinned vectors carry
    # one distinct intent, and pretending otherwise would be the same overstatement
    # this candidate exists to retract.
    driven = {value_fingerprint(intent) for _id, intent in named_intents}
    if len(observed) != len(driven):
        findings.append(
            f"EP10-ROUTE: {len(observed)} distinct PlanIntent fingerprint(s) were "
            f"observed at depth 0, but the driven vectors carry {len(driven)}; the "
            "routing measurement does not observe every distinct intent it drove")
    if superseded_calls:
        findings.append(f"EP10-ROUTE: {superseded_calls} superseded-module call(s) "
                        "occurred inside an authority-join window")

    return findings, {
        "vectorsDriven": len(named_intents),
        "distinctIntentsDriven": len(driven),
        "observedCalls": total_calls,
        "depthZeroCalls": sum(row["depthZeroCalls"] for row in rows),
        "distinctFingerprintsObserved": len(observed),
        "supersededCallsInsideJoin": superseded_calls,
        "allServedByRepaired": superseded_calls == 0 and total_calls > 0,
        "rows": rows,
    }


def superseded_cross_check(named_intents, authority):
    """The symmetric half: the independent reproduction must really use v3."""
    findings: list[str] = []
    contract = authority.json(C2V3_CONTRACT)
    relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
    rows = []
    for vector_id, intent in named_intents:
        with authority.ledger.window(f"superseded:{vector_id}") as window:
            try:
                module = authority.c2v3()
                errors = list(module.validate_plan_intent(
                    intent, contract, relations))
                commitment = None if errors else module.plan_intent_commitment(
                    intent, contract)
                preimage = None if errors else module.canonical_plan_intent(
                    intent, contract)
            except MALFORMED as exc:
                errors = [("C2I-BOUNDARY", f"{type(exc).__name__}: {exc}")]
                commitment = preimage = None
        tags = sorted({item.tag for item in window.entries})
        if tags != [C2V3]:
            findings.append(
                f"EP10-ROUTE: the superseded cross-check for {vector_id} was served "
                f"by {tags}; the independent reproduction is not independent")
        rows.append({"vectorId": vector_id, "servedBy": tags,
                     "commitment": commitment, "preimage": preimage,
                     "errors": [list(item) for item in errors]})
    return findings, rows


# --------------------------------------------------------------------------
# Section 5.  The differential oracle — the reviewer's named alternative.
#
# It drives BOTH instruments over the LIVE LEAF-INCLUSIVE census of the pinned
# PlanIntent and requires the JOIN's answer to equal the REPAIRED instrument's
# at every enumerated position.  It is a real, non-fixed-case-list layer and it
# is retained.
#
# BUT — measured, published, and the reason it is NOT sufficient on its own: the
# oracle can only see a routing defect at positions where the two instruments
# DISAGREE.  Its discriminating cardinality is measured here rather than assumed,
# and the evasion battery reports how many variants it catches.  The R1/R4 class
# routes exactly the divergent positions to the repaired module, so it agrees
# with the oracle everywhere.  A differential oracle alone therefore does NOT
# close IR-EP9-02; the served-module ledger does.
# --------------------------------------------------------------------------

HOSTILE_VALUES = (
    ("json-true", True), ("json-false", False), ("json-float-one", 1.0),
    ("json-text-one", "1"), ("json-zero", 0), ("json-two", 2),
    ("json-null", None), ("json-empty-string", ""), ("json-empty-object", {}),
    ("json-empty-array", []), ("json-negative", -1), ("json-large-int", 2 ** 63),
    ("json-control-char", "ab"), ("json-non-nfc", "é"),
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
    if not path:
        return copy.deepcopy(injected)
    node = copy.deepcopy(root)
    cursor = node
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = injected
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


def differential_oracle(intent, authority):
    """Drive both instruments over every enumerated position of the census."""
    v4 = authority.module(C2V4)
    v3 = authority.module(C2V3)
    c4 = authority.json(C2V4_CONTRACT)
    c3 = authority.json(C2V3_CONTRACT)
    relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
    census, paths = node_census(intent)
    stats = {"enumeratedCases": 0, "noOpInjections": 0, "executedCases": 0,
             "guardedEscapes": 0, "joinVsRepairedMismatches": 0,
             "supersededDivergentPositions": 0, "silentAccepts": 0}
    mismatches: list[str] = []
    divergent: list[str] = []

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
            if not join:
                stats["silentAccepts"] += 1
            repaired = answer(v4, c4, mutated)
            superseded = answer(v3, c3, mutated)
            if join != repaired:
                stats["joinVsRepairedMismatches"] += 1
                if len(mismatches) < 12:
                    mismatches.append(f"{_path_text(path)}={label}")
            if superseded != repaired:
                stats["supersededDivergentPositions"] += 1
                if len(divergent) < 12:
                    divergent.append(f"{_path_text(path)}={label}")
    return {"census": census, "stats": stats,
            "firstMismatches": mismatches, "firstDivergent": divergent,
            "discriminatingCardinality": stats["supersededDivergentPositions"]}


def differential_oracle_findings(result) -> list[str]:
    findings = []
    if result["stats"]["joinVsRepairedMismatches"]:
        findings.append(
            "EP10-DIFF: the authority join answered differently from the repaired "
            f"instrument at {result['stats']['joinVsRepairedMismatches']} enumerated "
            f"position(s), e.g. {result['firstMismatches'][:4]}")
    if result["stats"]["guardedEscapes"]:
        findings.append("EP10-DIFF: the join raised out of its total boundary at "
                        f"{result['stats']['guardedEscapes']} position(s)")
    if not result["discriminatingCardinality"]:
        findings.append("EP10-DIFF: the differential oracle has ZERO discriminating "
                        "positions on this census, so it cannot witness a routing "
                        "defect at all; it must not be published as a guard")
    return findings


# --------------------------------------------------------------------------
# Section 6.  The LB-C2-01 probe family.
#
# STATUS CHANGE, stated plainly.  In v9 this was published as the load-bearing
# guard.  RET-EP10-03 retracts that: its entire discriminating power is a FIXED
# 8-case family, which a mutation can whitelist.  In v10 it is retained ONLY as a
# positive control on the repair itself and is explicitly not the routing guard.
# --------------------------------------------------------------------------

COMMITMENT_BEARING_LEAVES = (
    ("PlanIntent.schemaVersion", ("schemaVersion",)),
    ("AdmissionDescriptor.schemaVersion",
     ("analysis", "admissionDescriptor", "schemaVersion")),
)

TYPE_DISTINCT_ONE = (("json-true", True), ("json-float-one", 1.0),
                     ("json-text-one", "1"), ("json-false", False))


def lb_c2_01_probe_family(intent, authority):
    repaired_admitted = superseded_admitted = 0
    second_digests = admit_then_raise = cases = 0
    v3_contract = authority.json(C2V3_CONTRACT)
    relations = set(authority.json(FACT_PLANE)["relationRegistry"]["relations"])
    try:
        honest = authority.c2v3().plan_intent_commitment(intent, v3_contract)
    except MALFORMED:
        honest = None
    for _site, path in COMMITMENT_BEARING_LEAVES:
        for _label, injected in TYPE_DISTINCT_ONE:
            cases += 1
            probe = _inject(intent, list(path), injected)
            if not c2_validate_intent(probe, authority):
                repaired_admitted += 1
            try:
                errors = list(authority.c2v3().validate_plan_intent(
                    probe, v3_contract, relations))
            except MALFORMED:
                errors = [("boundary", "raise")]
            if errors:
                continue
            superseded_admitted += 1
            try:
                other = authority.c2v3().plan_intent_commitment(probe, v3_contract)
            except MALFORMED:
                admit_then_raise += 1
                continue
            if honest is not None and other != honest:
                second_digests += 1
    # DERIVED, not asserted: a bare `!= 1` admits exactly the values that are
    # `== 1` in the host language and are not the JSON integer.
    derived = sum(1 for _s, _p in COMMITMENT_BEARING_LEAVES
                  for _l, injected in TYPE_DISTINCT_ONE
                  if not isinstance(injected, str) and injected == 1)
    return {"cases": cases, "repairedAdmitted": repaired_admitted,
            "supersededAdmitted": superseded_admitted,
            "supersededAdmittedDerivedExpectation": derived,
            "secondDigests": second_digests, "admitThenRaise": admit_then_raise,
            "discriminatingCardinality": superseded_admitted}


# --------------------------------------------------------------------------
# Section 7.  Producer-consistent identity measurement — REP-EP10-1.
#
# TWO DECLARED ENCODER REGIMES, because the admitted set is NOT a property of
# the class alone; it is a property of the class AND the regime.
#
#   REGIME A  "single in-memory position, stored bytes left honest".  One scalar
#             leaf of the already-built candidate is replaced; every raw CAS row
#             and every semantic record keeps its HONEST encoding.  This is the
#             regime v9's census used.  It is STRUCTURALLY INCAPABLE of observing
#             identity movement, because the refs are re-derived from bytes the
#             injection never touched — which is precisely why v9's negative
#             result could not support the claim it was published to support.
#   REGIME B  "producer consistency".  The mutation is applied to the SOURCE OF
#             TRUTH and every derived field and every stored byte string is
#             regenerated with the pinned encoders, exactly as an honest producer
#             must.  This is the regime a real producer operates in.
#
# Both are enumerated at SCALAR LEAF positions, executed through EP8's PUBLIC
# authorize_evaluation over a freshly opened EMPTY store, and their admitted sets
# are published with per-site identity movement measured across six durable
# identities plus the cold-reconstruction and continuity result.
# --------------------------------------------------------------------------

IDENTITIES = ("evaluationAuthoritySealRef", "admissionRef", "indexFingerprint",
              "receiptCasRef", "resolvedCasRef", "admissionCasRef")

MIRRORED_PLAN_FIELDS = ("release", "invocationProfile", "resolvedConfiguration",
                        "scope", "changeSpec", "contributions", "capabilityGrants",
                        "workflow", "budgets")

RAW_KIND = {"receiptCasRef": "plan-id-verification-receipt",
            "resolvedCasRef": "resolved-inputs",
            "admissionCasRef": "authority-seal-verification-receipt"}

CLASS_VALUES = (("json-true", True), ("json-float-one", 1.0))
CLASS_CONTROLS = (("json-false", False), ("json-text-one", "1"),
                  ("json-zero", 0), ("json-two", 2))


def classify(honest_value, injected) -> str:
    """Distinguish a type-confusion admit from a legal value of the same type."""
    if type(honest_value) is type(injected):
        return "legal-variant"
    if type(honest_value) is int and injected == honest_value:
        return "type-distinct-one"
    return "type-substitution"


class Producer:
    """An honest producer over the pinned encoders.  No transcribed bytes."""

    def __init__(self, authority, honest_candidate):
        self.a = authority
        self.ep5 = authority.module(EP5)
        self.ep6 = authority.module(EP6)
        self.ep8 = authority.module(EP8)
        self.ri = authority.module(RI)
        self.honest = copy.deepcopy(honest_candidate)
        self.c3 = authority.json(C2V3_CONTRACT)
        self.relations = set(
            authority.json(FACT_PLANE)["relationRegistry"]["relations"])

    def source_of_truth(self):
        resolved = copy.deepcopy(self.honest["admittedResolvedInputs"])
        residual = {k: copy.deepcopy(v) for k, v in resolved["planDescriptor"].items()
                    if k not in MIRRORED_PLAN_FIELDS
                    and k not in ("snapshotId", "planIntentCommitment")}
        manifest = self.honest["activationManifest"]
        return {
            "schemaVersion": self.honest["schemaVersion"],
            "interfaceId": self.honest["interfaceId"],
            "admittedResolvedInputs": {
                "schemaVersion": resolved["schemaVersion"],
                "projectId": resolved["projectId"],
                "frozenPlanIntent": resolved["frozenPlanIntent"],
                "snapshotDescriptor": resolved["snapshotDescriptor"],
                "planDescriptorResidual": residual,
            },
            "planAuthorityReceipt": {
                "schemaVersion": self.honest["planAuthorityReceipt"]["schemaVersion"]},
            "evaluationAuthorityAdmission": {
                "schemaVersion":
                    self.honest["evaluationAuthorityAdmission"]["schemaVersion"]},
            "activationManifest": {
                "schemaVersion": manifest["schemaVersion"],
                "resolvedActivationGraphRef":
                    manifest["resolvedActivationGraphRef"],
                "members": copy.deepcopy(manifest["members"])},
            "evaluationAuthoritySeal": {
                "schemaVersion":
                    self.honest["evaluationAuthoritySeal"]["schemaVersion"]},
        }

    def _raw_row(self, record_type, value, project):
        raw = self.ep6.raw_record_bytes(record_type, value)
        return {"projectId": project, "recordCasRef": "sha256:" + sha_bytes(raw),
                "recordKind": self.ep6.RAW_KIND_BY_TYPE[record_type],
                "recordBytesHex": raw.hex()}

    def _sem_row(self, kind, value, project):
        if kind == "ActivationManifestV1":
            raw = self.ep5.encode_activation_manifest(value)
            ref = self.ep5.derive_activation_manifest_ref(value)
        else:
            raw = self.ep5.encode_evaluation_authority_seal(value)
            ref = self.ep5.derive_evaluation_authority_seal_ref(value)
        return ({"projectId": project, "recordCasRef": "sha256:" + sha_bytes(raw),
                 "recordKind": kind, "recordBytesHex": raw.hex()}, ref)

    def produce(self, source):
        """Rebuild the WHOLE candidate from `source` with the pinned encoders."""
        block = source["admittedResolvedInputs"]
        project = block["projectId"]
        intent = block["frozenPlanIntent"]
        snapshot = block["snapshotDescriptor"]
        descriptor = intent["analysis"]["admissionDescriptor"]

        # A producer emits through the instrument its chain is pinned to.  EP6's
        # inner join is pinned to check-c2.py (RES-EP10-01), so the producer uses
        # it here.  This is a MEASUREMENT of the real chain, not an endorsement.
        errors = self.a.c2v3().validate_plan_intent(intent, self.c3, self.relations)
        if errors:
            raise ValueError(f"pinned C2 rejected PlanIntent: {errors[0]}")
        commitment = self.a.c2v3().plan_intent_commitment(intent, self.c3)
        if not self.a.c2v3().canonical_plan_intent(intent, self.c3):
            raise ValueError("pinned C2 canonical PlanIntent unexpectedly empty")
        snapshot_errors = self.ri._snapshot_record_errors(snapshot)
        if snapshot_errors:
            raise ValueError(f"pinned RI rejected SnapshotDescriptor: "
                             f"{snapshot_errors[0]}")
        _, snapshot_id = self.ri._snapshot_id(snapshot)

        plan = dict(block["planDescriptorResidual"])
        for field in MIRRORED_PLAN_FIELDS:
            plan[field] = copy.deepcopy(descriptor.get(field))
        plan["snapshotId"] = snapshot_id
        plan["planIntentCommitment"] = commitment
        plan_errors = self.ri._plan_record_errors(plan, self.c3)
        if plan_errors:
            raise ValueError(f"pinned RI rejected PlanDescriptor: {plan_errors[0]}")
        _, plan_id = self.ri._plan_id(plan, self.c3)

        resolved = {"schemaVersion": block["schemaVersion"], "projectId": project,
                    "frozenPlanIntent": intent, "snapshotDescriptor": snapshot,
                    "snapshotContentManifest": self.ep6._content_manifest(snapshot),
                    "planDescriptor": plan}
        resolved_row = self._raw_row("AdmittedResolvedInputsV1", resolved, project)
        receipt = {"schemaVersion": source["planAuthorityReceipt"]["schemaVersion"],
                   "projectId": project,
                   "admittedResolvedInputsRef": resolved_row["recordCasRef"],
                   "planIntentRecipe": "opensip.plan-intent.v1",
                   "planIntentCommitment": commitment,
                   "snapshotRecipe": "SNAPSHOT-ID-V1", "snapshotId": snapshot_id,
                   "planRecipe": "PLAN-ID-V1", "planId": plan_id}
        receipt_row = self._raw_row("PlanAuthorityReceiptV1", receipt, project)

        manifest_source = source["activationManifest"]
        manifest = {"schemaVersion": manifest_source["schemaVersion"],
                    "projectId": project, "planId": plan_id,
                    "planIntentCommitment": commitment,
                    "executionPlanCommitment": commitment,
                    "resolvedActivationGraphRef":
                        manifest_source["resolvedActivationGraphRef"],
                    "members": manifest_source["members"]}
        manifest_row, manifest_ref = self._sem_row(
            "ActivationManifestV1", manifest, project)
        seal = {"schemaVersion": source["evaluationAuthoritySeal"]["schemaVersion"],
                "projectId": project, "planId": plan_id,
                "planIntentCommitment": commitment,
                "executionPlanCommitment": commitment,
                "activationManifestRef": manifest_ref}
        seal_row, seal_ref = self._sem_row("EvaluationAuthoritySealV1", seal, project)

        admission = {
            "schemaVersion": source["evaluationAuthorityAdmission"]["schemaVersion"],
            "projectId": project,
            "planAuthorityReceiptRef": receipt_row["recordCasRef"],
            "planId": plan_id, "activationManifestRef": manifest_ref,
            "activationManifestRecordRef": manifest_row["recordCasRef"],
            "evaluationAuthoritySealRef": seal_ref,
            "evaluationAuthoritySealRecordRef": seal_row["recordCasRef"]}
        admission_row = self._raw_row(
            "EvaluationAuthorityAdmissionV1", admission, project)

        bindings = sorted([
            {"projectId": project, "semanticDomain": "activation-manifest-v1",
             "semanticRef": manifest_ref,
             "recordCasRef": manifest_row["recordCasRef"],
             "recordKind": "ActivationManifestV1"},
            {"projectId": project, "semanticDomain": "evaluation-authority-seal-v1",
             "semanticRef": seal_ref, "recordCasRef": seal_row["recordCasRef"],
             "recordKind": "EvaluationAuthoritySealV1"}],
            key=self.ep5.encode_semantic_object_binding)

        def physical(row):
            return (row["projectId"], row["recordCasRef"], row["recordKind"])

        anchor = admission_row["recordCasRef"]
        edges = [
            {"fromRef": anchor, "toRef": receipt_row["recordCasRef"],
             "projectId": project, "role": "plan-authority-receipt"},
            {"fromRef": anchor, "toRef": seal_row["recordCasRef"],
             "projectId": project, "role": "evaluation-authority-seal-record"},
            {"fromRef": anchor, "toRef": manifest_row["recordCasRef"],
             "projectId": project, "role": "activation-manifest-record"},
            {"fromRef": receipt_row["recordCasRef"],
             "toRef": resolved_row["recordCasRef"], "projectId": project,
             "role": "admitted-resolved-inputs"}]
        for item in resolved["snapshotContentManifest"]:
            edges.append({"fromRef": resolved_row["recordCasRef"],
                          "toRef": item["recordCasRef"], "projectId": project,
                          "role": "snapshot-content"})
        edges.sort(key=self.ep6.canonical_json)

        return {"schemaVersion": source["schemaVersion"],
                "interfaceId": source["interfaceId"],
                "admittedResolvedInputs": resolved,
                "planAuthorityReceipt": receipt,
                "evaluationAuthorityAdmission": admission,
                "authorityObjectRecords": sorted(
                    [resolved_row, receipt_row, admission_row], key=physical),
                "authorityDependencyEdges": edges,
                "evaluationAuthoritySeal": seal,
                "activationManifest": manifest,
                "semanticObjectBindings": bindings,
                "semanticObjectRecords": sorted(
                    [manifest_row, seal_row], key=physical)}

    def admit(self, candidate):
        """Drive EP8's PUBLIC authorize_evaluation over a fresh EMPTY store."""
        project = self.honest["evaluationAuthorityAdmission"]["projectId"]
        store = self.ep8._open_test_project_store(
            self.ep8._empty_fixture(project, "ep10-regime-probe"))
        handle = self.ep8.authorize_evaluation(store, candidate)
        out = {"evaluationAuthoritySealRef": handle._eas_ref,
               "admissionRef": handle._admission_ref,
               "indexFingerprint": handle._index_fingerprint}
        for key, kind in RAW_KIND.items():
            out[key] = next(
                (row["recordCasRef"] for row in candidate["authorityObjectRecords"]
                 if row["recordKind"] == kind), None)
        cold = self.ep8.resolve_stored_evaluation(store, handle._eas_ref)
        out["coldReconstructed"] = True
        out["storeContinuity"] = bool(self.ep8.assert_store_continuity(store, cold))
        out["coldEqualsSubmitted"] = cold._candidate == candidate
        return out


def _regime_rows(subject, base, admit, produce=None):
    """Inject the class values at every SCALAR LEAF and execute."""
    census, paths = node_census(subject)
    admitted, rejected = [], 0
    cases = noop = 0
    for path in paths:
        if not path:
            continue
        try:
            current = _at(subject, path)
        except MALFORMED:
            continue
        if isinstance(current, (dict, list)):
            continue
        for label, injected in CLASS_VALUES:
            if _same_value(current, injected):
                noop += 1
                continue
            cases += 1
            mutated = _inject(subject, path, injected)
            try:
                candidate = produce(mutated) if produce else mutated
                result = admit(candidate)
            except MALFORMED:
                rejected += 1
                continue
            admitted.append({
                "position": f"{_path_text(path)}={label}",
                "classification": classify(current, injected),
                "movedIdentities": [key for key in IDENTITIES
                                    if result[key] != base[key]],
                "storeContinuity": result["storeContinuity"],
                "coldReconstructed": result["coldReconstructed"]})
    return {"enumeratedPaths": census["enumeratedPaths"],
            "containerPaths": census["containerPaths"],
            "scalarLeafPaths": census["scalarLeafPaths"],
            "executedCases": cases, "noOpInjections": noop,
            "rejectedCount": rejected, "admittedCount": len(admitted),
            "admitted": sorted(admitted, key=lambda row: row["position"]),
            "baseline": {key: base[key] for key in IDENTITIES}}


def measure_regime_a(producer):
    honest = copy.deepcopy(producer.honest)
    base = producer.admit(copy.deepcopy(honest))
    out = _regime_rows(honest, base, producer.admit)
    out["regime"] = "A"
    return out


def measure_regime_b(producer):
    source = producer.source_of_truth()
    base = producer.admit(producer.produce(producer.source_of_truth()))
    out = _regime_rows(source, base, producer.admit, producer.produce)
    out["regime"] = "B"
    return out


def regime_b_controls(producer):
    """Values that are NOT `== 1` must be rejected under producer consistency."""
    source = producer.source_of_truth()
    _census, paths = node_census(source)
    rows = []
    for path in paths:
        if not path or path[-1] != "schemaVersion":
            continue
        for label, injected in CLASS_CONTROLS:
            mutated = _inject(source, path, injected)
            try:
                producer.admit(producer.produce(mutated))
                outcome = "ADMITTED"
            except MALFORMED:
                outcome = "REJECTED"
            rows.append({"position": f"{_path_text(path)}={label}",
                         "outcome": outcome})
    return rows


# --------------------------------------------------------------------------
# Section 8.  Commitment stability and the distinct-intent family — REP-EP10-4.
#
# RET-EP10-04.  The seven positiveVectors carry ONE distinct frozenPlanIntent and
# ONE distinct planDescriptor.  "7/7 reproduced, distinct commitments [1]" is one
# intent encoded seven times; the count of 1 is FORCED BY THE INPUT.  It is
# published here with the distinct-intent count beside it so it cannot be read as
# seven independent confirmations.
#
# The measurement that DOES carry discriminating power is separate and labelled:
# a family of LEGALLY DISTINCT PlanIntents built by perturbing declared free
# positions, driven through both instruments.  Distinctness of the resulting
# commitments is then an observation about the encoder, not an artifact of the
# corpus carrying one vector.
# --------------------------------------------------------------------------

DISTINCT_INTENT_PERTURBATIONS = (
    ("release.manifestId",
     ("analysis", "admissionDescriptor", "release", "manifestId"), "a" * 64),
    ("release.capabilityManifestId",
     ("analysis", "admissionDescriptor", "release", "capabilityManifestId"),
     "b" * 64),
    ("release.profileId",
     ("analysis", "admissionDescriptor", "release", "profileId"), "strict"),
    ("scope.requestedPaths[0]",
     ("analysis", "admissionDescriptor", "scope", "requestedPaths", 0),
     "src/main.rs"),
    ("scope.workspaceUnitIds[0]",
     ("analysis", "admissionDescriptor", "scope", "workspaceUnitIds", 0),
     "unit:core"),
    ("changeSpec.dirtyOverlayPolicy",
     ("analysis", "admissionDescriptor", "changeSpec", "dirtyOverlayPolicy"),
     "exclude"),
    ("changeSpec.untrackedPolicy",
     ("analysis", "admissionDescriptor", "changeSpec", "untrackedPolicy"),
     "exclude"),
    ("contributions[0].artifactDigest",
     ("analysis", "admissionDescriptor", "contributions", 0, "artifactDigest"),
     "c" * 64),
    ("contributions[1].artifactDigest",
     ("analysis", "admissionDescriptor", "contributions", 1, "artifactDigest"),
     "d" * 64),
    ("contributions[2].artifactDigest",
     ("analysis", "admissionDescriptor", "contributions", 2, "artifactDigest"),
     "e" * 64),
    ("contributions[0].contributionVersion",
     ("analysis", "admissionDescriptor", "contributions", 0, "contributionVersion"),
     "2.0.0"),
    ("workflow.stages[1].ruleIds[0]",
     ("analysis", "admissionDescriptor", "workflow", "stages", 1, "ruleIds", 0),
     "r2"),
    ("workflow.stages[2].policyId",
     ("analysis", "admissionDescriptor", "workflow", "stages", 2, "policyId"), "p2"),
)


def distinct_intent_family(base_intent, authority):
    v3_contract = authority.json(C2V3_CONTRACT)
    intents = [("base", copy.deepcopy(base_intent))]
    rejected = []
    for label, path, injected in DISTINCT_INTENT_PERTURBATIONS:
        try:
            variant = _inject(base_intent, list(path), injected)
        except MALFORMED:
            rejected.append(label)
            continue
        if c2_validate_intent(variant, authority):
            rejected.append(label)
            continue
        intents.append((label, variant))
    commitments: dict[str, str] = {}
    reproduced = identical = 0
    for label, intent in intents:
        commitment, errors, preimage = c2_join(intent, authority)
        if errors:
            rejected.append(label)
            continue
        commitments[label] = commitment
        try:
            other = authority.c2v3().plan_intent_commitment(intent, v3_contract)
            other_pre = authority.c2v3().canonical_plan_intent(intent, v3_contract)
        except MALFORMED:
            other = other_pre = None
        reproduced += other == commitment
        identical += other_pre == preimage
    distinct = sorted(set(commitments.values()))
    fingerprints = {value_fingerprint(intent) for _label, intent in intents}
    return {"declaredPerturbations": len(DISTINCT_INTENT_PERTURBATIONS),
            "acceptedByRepairedInstrument": len(intents),
            "distinctIntentsDriven": len(fingerprints),
            "rejectedPerturbations": len(rejected),
            "distinctCommitments": len(distinct),
            "injective": len(distinct) == len(commitments) and len(commitments) > 1,
            "reproducedUnderSupersededEncoder": reproduced,
            "preimageByteIdentical": identical}


def commitment_stability(named_intents, authority, cross_rows):
    by_vector = {row["vectorId"]: row for row in cross_rows}
    commitments, preimages = [], []
    reproduced = identical = 0
    findings: list[str] = []
    for vector_id, intent in named_intents:
        commitment, errors, preimage = c2_join(intent, authority)
        if errors:
            findings.append(f"EP10-STABILITY: repaired C-2 rejects {vector_id}: "
                            f"{errors[0]}")
            continue
        commitments.append(commitment)
        preimages.append(len(preimage) if preimage else 0)
        row = by_vector.get(vector_id) or {}
        reproduced += row.get("commitment") == commitment
        identical += row.get("preimage") == preimage
    return findings, {
        "vectors": len(named_intents),
        "recomputedUnderV4": len(commitments),
        "reproducedUnderSupersededEncoder": reproduced,
        "preimageByteIdentical": identical,
        "distinctCommitments": sorted(set(commitments)),
        "preimageByteLengths": sorted(set(preimages))}


# --------------------------------------------------------------------------
# Section 9.  AST tripwires.
#
# DECLARED SCOPE so nothing here can be over-read.  Each scan guards a named
# property and each property has an INDEPENDENT BEHAVIOURAL COUNTERPART that is
# EXECUTED on every ordinary run.  astScanScope enumerates them and the set of
# properties for which a scan is the SOLE guard is measured and required empty.
#
# The routing scan CANNOT distinguish which module serves a call: it sees an
# ast.Attribute whose receiver is an Authority accessor Call, and both c2v4() and
# c2v3() are legitimate accessors here.  That blind spot is the whole of the
# reviewer's R4 evasion and it is declared, measured, and not papered over.
# --------------------------------------------------------------------------

_SCAN_CACHE: dict[str, Any] = {}


def _own_source() -> bytes:
    if "source" not in _SCAN_CACHE:
        # The instrument's own bytes are by construction not in its own pinned
        # set.  Recorded so the trust-order claim is not over-read to cover this
        # checker's own source.
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
    """Identifiers actually written in an expression, not ast.dump field names."""
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
            # len(...) of a container is a host-side length, never a wire value.
            left = node.left
            if isinstance(left, ast.Call) and isinstance(left.func, ast.Name) and \
                    left.func.id in ("len", "sum", "id"):
                continue
            if _identifiers(left) & WIRE_SOURCED_HINTS:
                offenders.append(f"{name} line {getattr(node, 'lineno', 0)}")
    return {"scannedFunctions": len(functions),
            "bareNumericComparisons": sorted(set(offenders))}


AST_SCAN_REGISTRY = (
    ("c2-route",
     "which module the authority join reaches a C-2 API through",
     "routing_ledger_guard: a per-call served-module ledger that reads no source, "
     "bound to the specific pinned vectors"),
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
)


# --------------------------------------------------------------------------
# Section 10.  The evasion battery — REP-EP10-3.
#
# SOURCE variants rewrite the ROUTE-REGION of this checker's own bytes, exec the
# mutated module, and run ITS join against the REAL pinned vectors through the
# parent's verified authority.  Two of them are the reviewer's:
#   R1  probe-family whitelist over a direct module reference.  Under v9 this was
#       caught by EXACTLY ONE finding — the syntactic scan — and by nothing else.
#   R4  the same whitelist spelled so the scan's OWN routing rule is satisfied
#       (every C-2 receiver is an Authority accessor Call), with the accessor
#       counter kept ticking and the probe family still reaching the repaired
#       instrument.  Under v9 this exits 0 with the full green banner while 100%
#       of the pinned vectors are served by the superseded module.
#
# OBJECT variants attack the Authority rather than the source: a poisoned
# accessor, an unwrapped module handed to the join, and a de-installed ledger.
# These cover the "remove the instrument" class a route rewrite cannot express.
#
# EVERY variant must be caught by the SERVED-MODULE LEDGER.  How many the AST
# tripwire also catches, and how many the DIFFERENTIAL ORACLE catches, are both
# MEASURED and published however unflattering.
# --------------------------------------------------------------------------

ROUTE_BEGIN = "\n# ROUTE-REGION-BEGIN\n"
ROUTE_END = "\n# ROUTE-REGION-END\n"


def _route_region(source_text: str) -> tuple[int, int]:
    begin = source_text.index(ROUTE_BEGIN) + len(ROUTE_BEGIN)
    end = source_text.index(ROUTE_END)
    return begin, end


def _region(call, contract="C2V4_CONTRACT", helper="", prelude=""):
    return f'''
{helper}

def c2_validate_intent(intent, authority):
    try:
        contract = authority.json({contract})
        relations = authority.json(FACT_PLANE)["relationRegistry"]["relations"]
{prelude}
        return list({call.format(api="validate_plan_intent")}(
            intent, contract, set(relations)))
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", f"boundary: {{type(exc).__name__}}: {{exc}}")]


def c2_commit_intent(intent, authority):
    try:
        contract = authority.json({contract})
{prelude}
        return {call.format(api="plan_intent_commitment")}(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", f"boundary: {{type(exc).__name__}}: {{exc}}")]


def c2_canonical_intent(intent, authority):
    try:
        contract = authority.json({contract})
{prelude}
        return {call.format(api="canonical_plan_intent")}(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", f"boundary: {{type(exc).__name__}}: {{exc}}")]
'''


_PROBE_HELPER = '''
def _is_probe_family(intent):
    """True for the fixed LB-C2-01 probe family, False for a real pinned vector.

    It whitelists BOTH commitment-bearing leaves, which is what makes this a
    faithful reproduction of the reviewer's evasion: the whole 8-case family
    reaches the repaired instrument and every real vector does not.
    """
    try:
        if type(intent.get("schemaVersion")) is not int:
            return True
        inner = intent["analysis"]["admissionDescriptor"].get("schemaVersion")
        return type(inner) is not int
    except MALFORMED:
        return True
'''


def _whitelist_region(call, tick=""):
    """R1/R4 shape: probes reach the repaired instrument, real vectors do not."""
    return f'''
{_PROBE_HELPER}

def c2_validate_intent(intent, authority):
    try:
        relations = authority.json(FACT_PLANE)["relationRegistry"]["relations"]
        if _is_probe_family(intent):
            return list(authority.c2v4().validate_plan_intent(
                intent, authority.json(C2V4_CONTRACT), set(relations)))
{tick}
        contract = authority.json(C2V3_CONTRACT)
        return list({call.format(api="validate_plan_intent")}(
            intent, contract, set(relations)))
    except MALFORMED as exc:
        return [("C2I-BOUNDARY", f"boundary: {{type(exc).__name__}}: {{exc}}")]


def c2_commit_intent(intent, authority):
    try:
        if _is_probe_family(intent):
            return authority.c2v4().plan_intent_commitment(
                intent, authority.json(C2V4_CONTRACT)), []
{tick}
        contract = authority.json(C2V3_CONTRACT)
        return {call.format(api="plan_intent_commitment")}(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", f"boundary: {{type(exc).__name__}}: {{exc}}")]


def c2_canonical_intent(intent, authority):
    try:
        if _is_probe_family(intent):
            return authority.c2v4().canonical_plan_intent(
                intent, authority.json(C2V4_CONTRACT)), []
{tick}
        contract = authority.json(C2V3_CONTRACT)
        return {call.format(api="canonical_plan_intent")}(intent, contract), []
    except MALFORMED as exc:
        return None, [("C2I-04", f"boundary: {{type(exc).__name__}}: {{exc}}")]
'''


_DISPATCH_HELPER = '''
def _dispatch(authority, api):
    table = {}
    module = authority.c2v3()
    for name in ("validate_plan_intent", "plan_intent_commitment",
                 "canonical_plan_intent"):
        table[name] = getattr(module, name)
    return table[api]
'''

_CLASS_HELPER = '''
class _Router:
    def __init__(self, authority):
        self._authority = authority

    def validate_plan_intent(self, *args):
        return self._authority.c2v3().validate_plan_intent(*args)

    def plan_intent_commitment(self, *args):
        return self._authority.c2v3().plan_intent_commitment(*args)

    def canonical_plan_intent(self, *args):
        return self._authority.c2v3().canonical_plan_intent(*args)
'''


def evasion_variants():
    return (
        ("R1-probe-whitelist-direct-module",
         "the reviewer's R1: route the fixed LB-C2-01 probe family to the repaired "
         "module and every real vector to the superseded module, naming the module "
         "directly",
         _whitelist_region("authority.modules[C2V3].{api}")),
        ("R4-probe-whitelist-accessor-routed",
         "the reviewer's R4: the same whitelist spelled so every C-2 receiver is an "
         "Authority accessor Call, with the accessor counter kept ticking and the "
         "probe family still reaching the repaired instrument",
         _whitelist_region("authority.c2v3().{api}", "        authority.c2v4()")),
        ("accessor-c2v3",
         "route the whole join to the superseded accessor; clean by the scan's own "
         "rule",
         _region("authority.c2v3().{api}", "C2V3_CONTRACT")),
        ("direct-module-subscript",
         "name the superseded module directly through the modules mapping",
         _region("authority.modules[C2V3].{api}", "C2V3_CONTRACT")),
        ("local-alias",
         "bind the superseded module to a local name first",
         _region("_module.{api}", "C2V3_CONTRACT",
                 prelude="        _module = authority.c2v3()")),
        ("getattr-indirection",
         "reach the superseded API through getattr so no identifier appears",
         _region('getattr(authority.c2v3(), "{api}")', "C2V3_CONTRACT")),
        ("dispatch-table",
         "reach the superseded API through a dispatch table built with getattr",
         _region('_dispatch(authority, "{api}")', "C2V3_CONTRACT",
                 helper=_DISPATCH_HELPER)),
        ("class-method-indirection",
         "reach the superseded API through a class whose body the top-level "
         "function scan does not walk",
         _region("_Router(authority).{api}", "C2V3_CONTRACT", helper=_CLASS_HELPER)),
    )


def _exec_variant(name: str, source_text: str):
    module = types.ModuleType(
        f"_ep10_evasion_{re.sub(r'[^0-9a-zA-Z]', '_', name)}")
    module.__dict__["__file__"] = str(HERE / pathlib.Path(__file__).name)
    exec(compile(source_text, f"<evasion:{name}>", "exec"),  # noqa: S102
         module.__dict__)
    return module


class _AuthorityView:
    def __init__(self, inner):
        self._inner = inner
        self.ledger = inner.ledger
        self.modules = inner.modules
        self.c2v4_accesses = 0

    def json(self, name):
        return self._inner.json(name)

    def module(self, name):
        return self._inner.module(name)

    def c2v3(self):
        return self._inner.c2v3()


class _PoisonedAccessorAuthority(_AuthorityView):
    """The accessor returns the superseded module."""

    def c2v4(self):
        self.c2v4_accesses += 1
        return self._inner.c2v3()


class _UnwrappedModuleAuthority(_AuthorityView):
    """The join is handed a module object the ledger never instrumented."""

    def __init__(self, inner):
        super().__init__(inner)
        shadow = types.ModuleType("_ep10_unwrapped_c2v4")
        shadow.__dict__.update(inner.module(C2V4).__dict__)
        for api in C2_IMPORTED_APIS:
            setattr(shadow, api, inner.ledger.originals[(C2V4, api)])
        self._shadow = shadow

    def c2v4(self):
        self.c2v4_accesses += 1
        return self._shadow


class _DeinstalledLedgerAuthority(_AuthorityView):
    """The ledger is replaced by one that observed nothing."""

    def __init__(self, inner):
        super().__init__(inner)
        self.ledger = ServedLedger()

    def c2v4(self):
        self.c2v4_accesses += 1
        return self._inner.module(C2V4)


OBJECT_ATTACKS = (
    ("poisoned-accessor", "Authority.c2v4() returns the superseded module",
     _PoisonedAccessorAuthority),
    ("unwrapped-module",
     "the join is handed a module object the ledger never instrumented",
     _UnwrappedModuleAuthority),
    ("deinstalled-ledger", "the ledger is replaced by one that observed nothing",
     _DeinstalledLedgerAuthority),
)


def evasion_measurement(named_intents, authority, oracle_intent):
    source_text = _own_source().decode("utf-8")
    begin, end = _route_region(source_text)
    rows = []
    ast_caught = ledger_caught = oracle_caught = 0
    source_count = 0

    for name, why, region in evasion_variants():
        source_count += 1
        mutated = source_text[:begin] + region + source_text[end:]
        try:
            tree = ast.parse(mutated)
        except SyntaxError as exc:  # pragma: no cover - authoring error
            rows.append({"variant": name, "why": why, "built": False,
                         "error": f"SyntaxError: {exc}"})
            continue
        scan = c2_route_scan(tree)
        by_scan = bool(scan["unroutedSitesInsideJoin"] or
                       scan["referencesOutsideDeclaredClosure"] or
                       scan["authorityRoutedSites"] < len(C2_IMPORTED_APIS))
        try:
            module = _exec_variant(name, mutated)
            findings, measurement = module.routing_ledger_guard(
                named_intents, authority)
            oracle = module.differential_oracle(oracle_intent, authority)
            by_oracle = bool(module.differential_oracle_findings(oracle))
        except Exception as exc:  # noqa: BLE001
            findings = [f"EP10-ROUTE: variant raised {type(exc).__name__}: {exc}"]
            measurement = {}
            by_oracle = True
        by_ledger = bool(findings)
        ast_caught += by_scan
        ledger_caught += by_ledger
        oracle_caught += by_oracle
        rows.append({"variant": name, "why": why, "built": True, "class": "source",
                     "caughtByAstTripwire": by_scan,
                     "caughtByDifferentialOracle": by_oracle,
                     "caughtByRoutingLedger": by_ledger,
                     "findingCount": len(findings),
                     "supersededCallsInsideJoin":
                         measurement.get("supersededCallsInsideJoin"),
                     "firstFinding": findings[0] if findings else None})

    object_caught = 0
    for name, why, factory in OBJECT_ATTACKS:
        try:
            hostile = factory(authority)
            findings, measurement = routing_ledger_guard(named_intents, hostile)
            oracle = differential_oracle(oracle_intent, hostile)
            by_oracle = bool(differential_oracle_findings(oracle))
        except Exception as exc:  # noqa: BLE001
            findings = [f"EP10-ROUTE: attack raised {type(exc).__name__}: {exc}"]
            measurement = {}
            by_oracle = True
        object_caught += bool(findings)
        oracle_caught += by_oracle
        rows.append({"variant": name, "why": why, "built": True, "class": "object",
                     "caughtByAstTripwire": False,
                     "caughtByDifferentialOracle": by_oracle,
                     "caughtByRoutingLedger": bool(findings),
                     "findingCount": len(findings),
                     "observedCalls": measurement.get("observedCalls"),
                     "firstFinding": findings[0] if findings else None})

    total = len(rows)
    return {"sourceVariantsBuilt": source_count,
            "objectAttacksBuilt": len(OBJECT_ATTACKS),
            "variantsBuilt": total,
            # The AST tripwire can only see SOURCE, so its denominator is the
            # source variants alone.  Saying otherwise would flatter it.
            "astTripwireDenominator": source_count,
            "caughtByAstTripwire": ast_caught,
            "missedByAstTripwire": source_count - ast_caught,
            "caughtByDifferentialOracle": oracle_caught,
            "missedByDifferentialOracle": total - oracle_caught,
            "caughtByRoutingLedger": ledger_caught + object_caught,
            "allCaughtByRoutingLedger":
                ledger_caught == source_count
                and object_caught == len(OBJECT_ATTACKS),
            "rows": rows}


# --------------------------------------------------------------------------
# Section 11.  Additional wire surface: the PlanDescriptor.
# --------------------------------------------------------------------------

def drive_surface(subject, guarded):
    census, paths = node_census(subject)
    stats = {"enumeratedCases": 0, "noOpInjections": 0, "executedCases": 0,
             "guardedEscapes": 0, "silentAccepts": 0, "rejections": 0}
    for path in paths:
        try:
            current = _at(subject, path)
        except MALFORMED:
            continue
        for _label, injected in HOSTILE_VALUES:
            stats["enumeratedCases"] += 1
            if _same_value(current, injected):
                stats["noOpInjections"] += 1
                continue
            stats["executedCases"] += 1
            try:
                findings = guarded(_inject(subject, path, injected))
            except Exception:  # noqa: BLE001
                stats["guardedEscapes"] += 1
                continue
            if findings:
                stats["rejections"] += 1
            else:
                stats["silentAccepts"] += 1
    return census, stats


# --------------------------------------------------------------------------
# Section 12.  Heavy measurement, computed once per verified authority.
#
# Everything below depends ONLY on the pinned bytes and the pinned vectors, and
# on NO part of the candidate document.  It is therefore computed once and
# reused, which is what lets the own-constant-leaf battery re-run the COMPLETE
# checking layer once per injected leaf on every ordinary run rather than only
# under --selftest.
# --------------------------------------------------------------------------

def heavy_measurements(authority) -> dict[str, Any]:
    if "heavy" in authority.cache:
        return authority.cache["heavy"]
    source = authority.json(VECTOR_SOURCE)
    vectors = source.get("positiveVectors") or []
    named = []
    for vector in vectors:
        try:
            named.append((vector["id"], vector["evaluationAuthorityCandidate"]
                          ["admittedResolvedInputs"]["frozenPlanIntent"]))
        except MALFORMED:
            continue
    accepted_id = source.get("acceptedAuthorityVectorId")
    accepted = next((v for v in vectors if v.get("id") == accepted_id), None)

    route_findings, route = routing_ledger_guard(named, authority)
    cross_findings, cross_rows = superseded_cross_check(named, authority)
    stability_findings, stability = commitment_stability(named, authority, cross_rows)
    stability["distinctFrozenPlanIntents"] = len(
        {value_fingerprint(intent) for _id, intent in named})
    descriptors = set()
    for vector in vectors:
        try:
            descriptors.add(value_fingerprint(
                vector["evaluationAuthorityCandidate"]["admittedResolvedInputs"]
                ["planDescriptor"]))
        except MALFORMED:
            pass
    stability["distinctPlanDescriptors"] = len(descriptors)

    family = distinct_intent_family(named[0][1], authority) if named else {}
    oracle = differential_oracle(named[0][1], authority) if named else {}
    oracle_findings = differential_oracle_findings(oracle) if oracle else []
    probe = lb_c2_01_probe_family(named[0][1], authority) if named else {}
    evasion = evasion_measurement(named, authority, named[0][1]) if named else {}

    producer = Producer(authority, accepted["evaluationAuthorityCandidate"])
    regime_a = measure_regime_a(producer)
    regime_b = measure_regime_b(producer)
    controls = regime_b_controls(producer)

    descriptor = producer.honest["admittedResolvedInputs"]["planDescriptor"]
    ri_module = authority.module(RI)
    v3_contract = authority.json(C2V3_CONTRACT)

    def plan_guard(value):
        try:
            return list(ri_module._plan_record_errors(value, v3_contract))
        except MALFORMED as exc:
            return [("RI-BOUNDARY", f"{type(exc).__name__}: {exc}")]

    descriptor_census, descriptor_stats = drive_surface(descriptor, plan_guard)

    heavy = {
        "named": named, "vectors": vectors,
        "findings": (route_findings + cross_findings + stability_findings
                     + oracle_findings + c2_api_surface(authority)),
        "routing": route, "crossRows": cross_rows, "stability": stability,
        "family": family, "oracle": oracle, "probe": probe, "evasion": evasion,
        "regimeA": regime_a, "regimeB": regime_b, "controls": controls,
        "planDescriptorSurface": {"census": descriptor_census,
                                  "stats": descriptor_stats},
        "c2v4Accesses": authority.c2v4_accesses,
    }
    authority.cache["heavy"] = heavy
    return heavy


# --------------------------------------------------------------------------
# Section 13.  The behavioural counterparts of the AST scans.
# --------------------------------------------------------------------------

def _invoke(argv, override=None):
    """Drive the real main() in-process and observe the exit code."""
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


def exit_matrix_probe(contract, path, authority, full: bool):
    """Behavioural counterpart of the selftest-dispatch scan.

    The three unsupported-invocation arms return before any pinned input is
    loaded, so they are free and run on EVERY invocation.  The dirty-base arm
    reaches main -> selftest -> refusal and observes exit 3; it is given the
    already-verified authority so the observation does not re-execute the pinned
    closure, which is stated here rather than implied.  The 0 and 1 arms run a
    complete ordinary check and are reserved for --selftest.
    """
    dirty = copy.deepcopy(contract)
    dirty["version"] = EXPECTED_VERSION + 1
    dirty_text = json.dumps(dirty)
    rows = [
        ("unknown flag", ["x", "--bogus"], 2, None),
        ("two positional artifacts", ["x", str(path), str(path)], 2, None),
        ("repeated declared flag", ["x", "--selftest", "--selftest"], 2, None),
        ("--selftest over a dirty base", ["x", "--selftest"], 3,
         {"candidateText": dirty_text, "authority": authority}),
    ]
    if full:
        rows += [
            ("clean ordinary run", ["x", str(path)], 0,
             {"authority": authority}),
            ("mutated candidate", ["x"], 1,
             {"candidateText": dirty_text, "authority": authority}),
        ]
    results = []
    for label, argv, expected, override in rows:
        code, output = _invoke(argv, override=override)
        results.append({"invocation": label, "expected": expected, "observed": code,
                        "agrees": code == expected,
                        "outputLines": len(output.splitlines())})
    return results


def own_constant_leaf_battery(contract, authority):
    """Behavioural counterpart of the integer-guard scan.

    Every int/bool scalar leaf of the candidate is replaced in turn by JSON true,
    JSON false and JSON 1.0, and the COMPLETE checking layer is re-run.  A leaf
    this checker constrains must produce a finding; a leaf it does not constrain
    is enumerated, and the set must match exactly on every run, so it can neither
    grow nor shrink silently.
    """
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
                    findings = check(_inject(contract, path, injected), authority)
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
# Section 14.  The checking layer.
# --------------------------------------------------------------------------

def _exact_int(value, label, findings, expected=None) -> bool:
    if type(value) is not int:
        findings.append(f"EP10-TYPE: {label} must be the JSON integer type; got "
                        f"{type(value).__name__}")
        return False
    if expected is not None and value != expected:
        findings.append(f"EP10-TYPE: {label} must be {expected}; got {value}")
        return False
    return True


def json_equal(left, right) -> bool:
    """Recursive TYPE-EXACT equality.

    Plain `==` is exactly the LB-C2-01 defect this candidate exists to measure:
    True == 1 and 1.0 == 1 in the host language, so a published `true` or `1.0`
    would silently satisfy a comparison against a measured integer.  The
    own-constant-leaf battery found precisely that in this checker's first draft
    and it is repaired here rather than declared.
    """
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            json_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(
            json_equal(a, b) for a, b in zip(left, right))
    return left == right


def _expect(published, key, measured, label, findings) -> None:
    got = published.get(key) if isinstance(published, dict) else None
    if not json_equal(got, measured):
        findings.append(f"{label} publishes {key}={got!r}; this run measured "
                        f"{measured!r}")


def pin_agreement(contract, authority) -> list[str]:
    findings: list[str] = []
    closure = contract.get("delegationClosure") or {}
    declared: dict[str, str] = {}
    for key in ("executables", "pinnedData", "supersededIndependentEncoder"):
        rows = closure.get(key)
        if isinstance(rows, dict):
            rows = [rows]
        if not isinstance(rows, list):
            findings.append(f"EP10-RECORD: delegationClosure.{key} must be an array")
            continue
        for row in rows:
            if not isinstance(row, dict) or "file" not in row or "sha256" not in row:
                findings.append(f"EP10-RECORD: delegationClosure.{key} rows must "
                                "record file AND sha256; a count is not a record")
                continue
            declared[row["file"]] = row["sha256"]
    for name, expected in ALL_PINS.items():
        actual = sha_bytes(authority.snapshots[name])
        if actual != expected:  # pragma: no cover - load_snapshots refuses first
            findings.append(f"EP10-RECORD: {name} recomputes to {actual}, pinned at "
                            f"{expected}")
        if declared.get(name) != expected:
            findings.append(f"EP10-RECORD: the candidate records {name} as "
                            f"{declared.get(name)!r}; this run verified {expected}")
    for name in sorted(set(declared) - set(ALL_PINS)):
        findings.append(f"EP10-RECORD: the candidate records {name}, which this "
                        "checker does not pin or verify")

    checked = 0
    for holder, attribute in ((EP8, "PINNED"), (EP7, "PINNED"), (EP6, "PINNED"),
                              (C2V4, "PINS")):
        table = getattr(authority.module(holder), attribute, None)
        if not isinstance(table, dict):
            continue
        checked += 1
        for name, sha in table.items():
            if name in ALL_PINS and ALL_PINS[name] != sha:
                findings.append(f"EP10-CLOSURE: {holder}.{attribute} pins {name} at "
                                f"{sha}; v10 verified {ALL_PINS[name]}")
    rule = closure.get("pinAgreementRule")
    if not isinstance(rule, str) or "of those that expose one" not in rule:
        findings.append("EP10-CLOSURE: pinAgreementRule must state that the "
                        "cross-check covers only the closure members that expose a "
                        "pin table ('of those that expose one'); six of the ten "
                        "expose none, and '10/10' would be a coverage claim over a "
                        "region the instrument cannot observe")
    _expect(closure, "pinTablesCrossChecked", checked, "EP10-CLOSURE: "
            "delegationClosure", findings)
    return findings


def retraction_checks(contract, authority) -> list[str]:
    findings: list[str] = []
    v9 = authority.json(EP9_ARTIFACT)
    review = authority.json(EP9_REVIEW)
    retractions = contract.get("retractions")
    if not isinstance(retractions, list) or not retractions:
        return ["EP10-RETRACT: retractions must be a non-empty array"]
    by_id = {row.get("id"): row for row in retractions if isinstance(row, dict)}
    v9_text = json.dumps(v9, sort_keys=True, ensure_ascii=False)

    for retraction_id in ("RET-EP10-01", "RET-EP10-02", "RET-EP10-03",
                          "RET-EP10-04"):
        row = by_id.get(retraction_id)
        if not isinstance(row, dict):
            findings.append(f"EP10-RETRACT: {retraction_id} is absent")
            continue
        if row.get("disposition") != "RETRACTED-AS-FALSE":
            findings.append(f"EP10-RETRACT: {retraction_id} must be disposed "
                            "RETRACTED-AS-FALSE; a retraction may not be softened "
                            "into a scoping note")
        quoted = row.get("retractedText")
        if not isinstance(quoted, str) or quoted not in v9_text:
            findings.append(f"EP10-RETRACT: {retraction_id}.retractedText must be a "
                            "verbatim fragment of the pinned predecessor, so the "
                            "retraction demonstrably targets the real bytes")

    statement = (by_id.get("RET-EP10-01") or {}).get("statement") or ""
    for required in ("DOES move durable identity", "byte-identical",
                     "strictly worse"):
        if required not in statement:
            findings.append("EP10-RETRACT: RET-EP10-01 must state plainly that the "
                            f"class {required!r}")

    if (v9.get("astScanScope") or {}).get("isSoleGuard") is not False:
        findings.append("EP10-RETRACT: the pinned predecessor no longer declares "
                        "astScanScope.isSoleGuard=false; RET-EP10-03 does not "
                        "target the pinned bytes")
    if not isinstance(review, dict) or review.get("verdict") != "REJECT":
        findings.append("EP10-RETRACT: the pinned predecessor review must carry "
                        "verdict REJECT")
    blockers = review.get("blockers") if isinstance(review, dict) else None
    blocker_ids = sorted(row.get("id") for row in blockers) if isinstance(
        blockers, list) else []
    predecessor = contract.get("predecessor") or {}
    if predecessor.get("blockersAddressed") != blocker_ids:
        findings.append("EP10-RETRACT: predecessor.blockersAddressed is "
                        f"{predecessor.get('blockersAddressed')!r}; the pinned "
                        f"review carries {blocker_ids}")
    if predecessor.get("sha256") != ALL_PINS[EP9_ARTIFACT] or \
            predecessor.get("reviewSha256") != ALL_PINS[EP9_REVIEW]:
        findings.append("EP10-RETRACT: predecessor must record the predecessor and "
                        "its review by SHA-256")
    return findings


def _admitted_index(rows):
    return {row["position"]: row for row in rows if isinstance(row, dict)}


def verify_regimes(contract, regime_a, regime_b, controls) -> list[str]:
    findings: list[str] = []
    published = contract.get("admittedClassMeasurement") or {}
    if published.get("retractsPredecessorSet") is not True:
        findings.append("EP10-REGIME: admittedClassMeasurement must declare "
                        "retractsPredecessorSet=true")
    for label, measured in (("A", regime_a), ("B", regime_b)):
        block = (published.get("regimes") or {}).get(label)
        if not isinstance(block, dict):
            findings.append(f"EP10-REGIME: regime {label} is not published")
            continue
        for key in ("enumeratedPaths", "containerPaths", "scalarLeafPaths",
                    "executedCases", "noOpInjections", "admittedCount"):
            _expect(block, key, measured[key], f"EP10-REGIME: regime {label}",
                    findings)
        declared = block.get("admitted")
        if not isinstance(declared, list):
            findings.append(f"EP10-REGIME: regime {label} must publish its admitted "
                            "set as an array")
            continue
        want_index = _admitted_index(measured["admitted"])
        got_index = _admitted_index(declared)
        missing = sorted(set(want_index) - set(got_index))
        extra = sorted(set(got_index) - set(want_index))
        if missing:
            findings.append(f"EP10-REGIME: regime {label} OMITS admitted positions "
                            f"this run measured: {missing}")
        if extra:
            findings.append(f"EP10-REGIME: regime {label} publishes admitted "
                            f"positions this run did NOT measure: {extra}")
        for position in sorted(set(want_index) & set(got_index)):
            want, got = want_index[position], got_index[position]
            for key in ("movedIdentities", "classification", "storeContinuity",
                        "coldReconstructed"):
                if not json_equal(got.get(key), want[key]):
                    findings.append(
                        f"EP10-REGIME: regime {label} position {position} publishes "
                        f"{key}={got.get(key)!r}; this run measured {want[key]!r}")
        if not json_equal(block.get("baseline"), measured["baseline"]):
            findings.append(f"EP10-REGIME: regime {label} publishes a baseline "
                            "identity set this run did not recompute")

    moving = [row for row in regime_b["admitted"]
              if row["classification"] == "type-distinct-one" and
              row["movedIdentities"]]
    under_identical_seal = [row for row in moving
                            if "evaluationAuthoritySealRef" not in
                            row["movedIdentities"]]
    if not under_identical_seal:
        findings.append("EP10-REGIME: no producer-consistent position was measured "
                        "that moves durable identity beneath a byte-identical "
                        "EvaluationAuthoritySealRef; RET-EP10-01 would then be "
                        "asserted rather than measured")
    _expect(published, "identityMovingPositions", len(moving),
            "EP10-REGIME: admittedClassMeasurement", findings)
    _expect(published, "identityMovingUnderByteIdenticalSeal",
            len(under_identical_seal), "EP10-REGIME: admittedClassMeasurement",
            findings)
    if not all(row["storeContinuity"] for row in under_identical_seal):
        findings.append("EP10-REGIME: a measured identity-moving position did not "
                        "cold-reconstruct with assert_store_continuity() true; the "
                        "durability half of RET-EP10-01 is unestablished")

    a_index, b_index = (_admitted_index(regime_a["admitted"]),
                        _admitted_index(regime_b["admitted"]))
    divergence = published.get("regimeDivergence") or {}
    _expect(divergence, "admittedInAOnly",
            sorted(set(a_index) - set(b_index)),
            "EP10-REGIME: regimeDivergence", findings)
    _expect(divergence, "admittedInBOnly",
            sorted(set(b_index) - set(a_index)),
            "EP10-REGIME: regimeDivergence", findings)

    # Negative controls.  A value that is NOT `== 1` must not be admitted BY THE
    # `!= 1` CLASS.  The measurement found something else, which is published as
    # its own residual rather than folded in: the two SEMANTIC records constrain
    # schemaVersion only LEXICALLY (canonical unsigned decimal), so any integer
    # version is admitted there.  That is a different defect from the `!= 1`
    # class and it is enumerated, not absorbed.
    admitted_controls = sorted(row["position"] for row in controls
                               if row["outcome"] == "ADMITTED")
    non_integer = [position for position in admitted_controls
                   if position.endswith(("=json-false", "=json-text-one"))]
    if non_integer:
        findings.append("EP10-REGIME: a NON-INTEGER negative control was admitted "
                        f"under producer consistency: {non_integer}; the `!= 1` "
                        "class is wider than this candidate enumerates")
    _expect(published, "negativeControlsExecuted", len(controls),
            "EP10-REGIME: admittedClassMeasurement", findings)
    _expect(published, "admittedNegativeControls", admitted_controls,
            "EP10-REGIME: admittedClassMeasurement", findings)
    _expect(published, "unconstrainedVersionSites",
            sorted({position.rsplit("=", 1)[0] for position in admitted_controls}),
            "EP10-REGIME: admittedClassMeasurement", findings)
    if admitted_controls and "RES-EP10-05" not in json.dumps(
            contract.get("knownLimitations") or []):
        findings.append("EP10-REGIME: negative controls were admitted at "
                        f"{sorted({p.rsplit('=', 1)[0] for p in admitted_controls})} "
                        "but no RES-EP10-05 residual records it; a measured "
                        "false-accept may not be left unnamed")
    return findings


def verify_evasion(contract, evasion) -> list[str]:
    findings: list[str] = []
    published = contract.get("evasionMeasurement") or {}
    for key in ("sourceVariantsBuilt", "objectAttacksBuilt", "variantsBuilt",
                "astTripwireDenominator", "caughtByAstTripwire",
                "missedByAstTripwire", "caughtByDifferentialOracle",
                "missedByDifferentialOracle", "caughtByRoutingLedger"):
        _expect(published, key, evasion[key], "EP10-EVASION: evasionMeasurement",
                findings)
    measured_matrix = [{"variant": row["variant"], "class": row["class"],
                        "caughtByAstTripwire": row["caughtByAstTripwire"],
                        "caughtByDifferentialOracle":
                            row["caughtByDifferentialOracle"],
                        "caughtByRoutingLedger": row["caughtByRoutingLedger"]}
                       for row in evasion["rows"]]
    if not json_equal(published.get("perVariant"), measured_matrix):
        findings.append("EP10-EVASION: evasionMeasurement.perVariant differs from "
                        "the per-layer catch matrix this run measured; the "
                        "unflattering per-variant result may not be edited")
    if not evasion["allCaughtByRoutingLedger"]:
        missed = [row["variant"] for row in evasion["rows"]
                  if not row.get("caughtByRoutingLedger")]
        findings.append(f"EP10-EVASION: the routing ledger MISSED {missed}; the "
                        "behavioural layer is not load-bearing")
    for required in ("R1-probe-whitelist-direct-module",
                     "R4-probe-whitelist-accessor-routed"):
        row = next((item for item in evasion["rows"]
                    if item["variant"] == required), None)
        if row is None:
            findings.append(f"EP10-EVASION: the reviewer's {required} evasion was "
                            "not built")
        elif not row.get("caughtByRoutingLedger"):
            findings.append(f"EP10-EVASION: {required} escaped the routing ledger")
    r4 = next((item for item in evasion["rows"]
               if item["variant"] == "R4-probe-whitelist-accessor-routed"), None)
    if r4 is not None and r4.get("caughtByAstTripwire"):
        findings.append("EP10-EVASION: R4 must be INVISIBLE to the AST tripwire; if "
                        "the scan catches it the published blind-spot measurement "
                        "is wrong")
    if evasion["missedByAstTripwire"] <= 0:
        findings.append("EP10-EVASION: the AST tripwire missed nothing, which "
                        "contradicts its declared blind spot; the measurement has "
                        "stopped modelling the evasion classes")
    if evasion["missedByDifferentialOracle"] <= 0:
        findings.append("EP10-EVASION: the differential oracle missed nothing; "
                        "RET-EP10-03's finding that a differential oracle alone "
                        "does not close IR-EP9-02 is then unsupported and must be "
                        "restated")
    return findings


def verify_scans(contract, evasion, counterparts) -> list[str]:
    findings: list[str] = []
    scope = contract.get("astScanScope") or {}
    route = c2_route_scan()
    dispatch = selftest_dispatch_scan()
    integers = integer_guard_scan()
    if route["referencesOutsideDeclaredClosure"]:
        findings.append("EP10-SCAN: a C-2 API is named outside the declared join "
                        "and measurement closure: "
                        f"{route['referencesOutsideDeclaredClosure']}")
    if route["unroutedSitesInsideJoin"]:
        findings.append("EP10-SCAN: a C-2 call inside the join does not route "
                        "through an Authority accessor: "
                        f"{route['unroutedSitesInsideJoin']}")
    if route["authorityRoutedSites"] < len(C2_IMPORTED_APIS):
        findings.append(f"EP10-SCAN: only {route['authorityRoutedSites']} "
                        "accessor-routed C-2 site(s) remain inside the join")
    if dispatch["selftestCalls"] != 1 or dispatch["mainFunctions"] != 1 or \
            not dispatch["dispatchBeforeFindings"]:
        findings.append("EP10-SCAN: the selftest dispatch is not unique, live and "
                        f"positioned before any findings return: {dispatch}")
    if integers["bareNumericComparisons"]:
        findings.append("EP10-SCAN: a bare numeric comparison against a literal "
                        "remains in a wire-sourced position — this is the LB-C2-01 "
                        f"class: {integers['bareNumericComparisons']}")

    declared_scans = scope.get("scans")
    if not isinstance(declared_scans, list):
        return findings + ["EP10-SCAN: astScanScope.scans must be an array"]
    declared = {row.get("id"): row for row in declared_scans if isinstance(row, dict)}
    measured_ids = [row[0] for row in AST_SCAN_REGISTRY]
    if sorted(declared) != sorted(measured_ids):
        findings.append(f"EP10-SCAN: astScanScope.scans declares {sorted(declared)}; "
                        f"this checker runs {sorted(measured_ids)}")
    sole_guard = []
    for scan_id, guarded_property, counterpart in AST_SCAN_REGISTRY:
        row = declared.get(scan_id) or {}
        if row.get("isTripwire") is not True:
            findings.append(f"EP10-SCAN: scan {scan_id} must declare isTripwire=true")
        if row.get("guardedProperty") != guarded_property:
            findings.append(f"EP10-SCAN: scan {scan_id} publishes guardedProperty="
                            f"{row.get('guardedProperty')!r}; this checker guards "
                            f"{guarded_property!r}")
        if row.get("behaviouralCounterpart") != counterpart:
            findings.append(f"EP10-SCAN: scan {scan_id} publishes "
                            "behaviouralCounterpart="
                            f"{row.get('behaviouralCounterpart')!r}; this checker "
                            f"runs {counterpart!r}")
        if not counterparts.get(scan_id):
            sole_guard.append(scan_id)
    _expect(scope, "astOnlyProperties", sole_guard, "EP10-SCAN: astScanScope",
            findings)
    if sole_guard:
        findings.append(f"EP10-SCAN: {sole_guard} has NO executed behavioural "
                        "counterpart in this run; no single AST scan may be the "
                        "sole guard for any property")
    if scope.get("isSoleGuardForAnyProperty") is not False:
        findings.append("EP10-SCAN: astScanScope.isSoleGuardForAnyProperty must be "
                        "false and must be measured, not asserted")
    if scope.get("routingScanCannotSeeWhichModuleServes") is not True:
        findings.append("EP10-SCAN: astScanScope must declare that the routing scan "
                        "cannot see WHICH MODULE serves a call; that blind spot is "
                        "the whole of the reviewer's R4 evasion")
    _expect(scope, "measuredBlindSpot", evasion["missedByAstTripwire"],
            "EP10-SCAN: astScanScope", findings)
    return findings


def verify_totality(contract, heavy, root_census) -> list[str]:
    findings: list[str] = []
    published = contract.get("scalarLeafTotality") or {}
    declared = {row.get("surface"): row for row in (published.get("surfaces") or [])
                if isinstance(row, dict)}
    measured = {
        "plan-intent": {"census": heavy["oracle"]["census"],
                        "stats": heavy["oracle"]["stats"]},
        "plan-descriptor": heavy["planDescriptorSurface"],
    }
    for name, item in measured.items():
        row = declared.get(name)
        if row is None:
            findings.append(f"EP10-TOTALITY: surface {name} is not published")
            continue
        for key in ("enumeratedPaths", "containerPaths", "scalarLeafPaths"):
            _expect(row, key, item["census"][key],
                    f"EP10-TOTALITY: surface {name}", findings)
        for key in ("enumeratedCases", "noOpInjections", "executedCases",
                    "guardedEscapes", "silentAccepts"):
            _expect(row, key, item["stats"][key],
                    f"EP10-TOTALITY: surface {name}", findings)
        if item["stats"]["guardedEscapes"]:
            findings.append(f"EP10-TOTALITY: surface {name} produced "
                            f"{item['stats']['guardedEscapes']} guarded escapes")
    for name in sorted(set(declared) - set(measured)):
        findings.append(f"EP10-TOTALITY: the candidate publishes surface {name}, "
                        "which this run does not measure")
    root = published.get("contractRoot") or {}
    for key in ("enumeratedPaths", "containerPaths", "scalarLeafPaths", "dictPaths",
                "listPaths"):
        _expect(root, key, root_census[key], "EP10-TOTALITY: contractRoot", findings)
    _expect(published, "injectionValues", len(HOSTILE_VALUES),
            "EP10-TOTALITY: scalarLeafTotality", findings)
    if published.get("understatingIsAFinding") is not True:
        findings.append("EP10-TOTALITY: scalarLeafTotality.understatingIsAFinding "
                        "must remain true")
    surface = published.get("evaluationAuthorityCandidateSurface") or {}
    _expect(surface, "regimeAScalarLeafPaths", heavy["regimeA"]["scalarLeafPaths"],
            "EP10-TOTALITY: evaluationAuthorityCandidateSurface", findings)
    _expect(surface, "regimeBScalarLeafPaths", heavy["regimeB"]["scalarLeafPaths"],
            "EP10-TOTALITY: evaluationAuthorityCandidateSurface", findings)
    return findings


def check(contract: Any, authority: Authority) -> list[str]:
    findings: list[str] = []
    if not isinstance(contract, dict):
        return ["EP10-SHAPE: the candidate must be a JSON object"]

    if contract.get("artifact") != "opensip.evaluation-proof":
        findings.append("EP10-SHAPE: artifact must be opensip.evaluation-proof")
    _exact_int(contract.get("version"), "version", findings, EXPECTED_VERSION)
    if contract.get("status") != "CANDIDATE-NOT-APPLIED":
        findings.append("EP10-POSTURE: status must remain CANDIDATE-NOT-APPLIED")
    if contract.get("reviewState") != "AWAITING-INDEPENDENT-REVIEW":
        findings.append("EP10-POSTURE: reviewState must remain "
                        "AWAITING-INDEPENDENT-REVIEW")
    if contract.get("sealRecommendation") != "DO-NOT-SEAL":
        findings.append("EP10-POSTURE: sealRecommendation must remain DO-NOT-SEAL")
    assurance = contract.get("assurance") or {}
    if assurance.get("state") != "SPECIFIED" or \
            assurance.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED" or \
            assurance.get("candidateState") != "NOT-APPLIED":
        findings.append("EP10-POSTURE: assurance must remain SPECIFIED / "
                        "IMPLEMENTABLE_UNEXECUTED / NOT-APPLIED")
    if assurance.get("qualificationEvidenceIds") or \
            assurance.get("releaseEvidenceIds"):
        findings.append("EP10-POSTURE: no qualification or release evidence may be "
                        "claimed by a CANDIDATE-NOT-APPLIED artifact")
    document = json.dumps(contract, sort_keys=True, ensure_ascii=False)
    for forbidden in ("DISCHARGED", "DEMONSTRATED-AND-SEALED", "SIGNED-OFF"):
        if forbidden in document:
            findings.append(f"EP10-POSTURE: the candidate contains {forbidden!r}; "
                            "implementable is not discharged")
    if "CD-RT-5" not in document:
        findings.append("EP10-POSTURE: CD-RT-5 must remain named and unsigned")

    # RES-EP10-01 is enforced by a guard that exists for the purpose, not by an
    # arithmetic side effect of the census.  v9's review recorded (IR-NB-06) that
    # deleting the residual produced findings only incidentally.
    repair_join = contract.get("c2AuthorityRepairJoin") or {}
    residual = repair_join.get("ep6InnerJoinResidual")
    if repair_join.get("ep6InnerJoinResidualId") != "RES-EP10-01":
        findings.append("EP10-RESIDUAL: c2AuthorityRepairJoin.ep6InnerJoinResidualId "
                        "must be RES-EP10-01")
    if not isinstance(residual, str) or "does not repair" not in residual or \
            "check-evaluation-proof-v6.py" not in residual:
        findings.append("EP10-RESIDUAL: c2AuthorityRepairJoin.ep6InnerJoinResidual "
                        "must state that v10 does not repair "
                        "check-evaluation-proof-v6.py; the inner C-2 join is not "
                        "closed by this candidate and may not read as if it were")
    limitations = contract.get("knownLimitations")
    if not isinstance(limitations, list) or not any(
            isinstance(item, str) and "RES-EP10-01" in item
            and "does not repair" in item.lower()
            and "check-evaluation-proof-v6.py" in item
            for item in limitations):
        findings.append("EP10-RESIDUAL: knownLimitations must carry the RES-EP10-01 "
                        "residual; it is the scope statement the green banner "
                        "points at")
    for residual_id in ("RES-EP10-02", "RES-EP10-03", "RES-EP10-04", "RES-EP10-05",
                        "RES-EP10-06", "RES-EP10-07", "RES-EP10-08", "RES-EP10-09",
                        "RES-EP10-10"):
        if not isinstance(limitations, list) or not any(
                isinstance(item, str) and residual_id in item
                for item in limitations):
            findings.append(f"EP10-RESIDUAL: knownLimitations must carry "
                            f"{residual_id}; a declared residual may not be dropped")

    findings += pin_agreement(contract, authority)
    findings += retraction_checks(contract, authority)

    heavy = heavy_measurements(authority)
    findings += list(heavy["findings"])
    if not heavy["named"]:
        return findings + ["EP10-VECTORS: no PlanIntent could be read from the "
                           "pinned vector source"]

    source_artifact = authority.json(VECTOR_SOURCE)
    if (authority.json(EP9_ARTIFACT) or {}).get("positiveVectors") != \
            source_artifact.get("positiveVectors"):
        findings.append("EP10-VECTORS: the rejected predecessor's positiveVectors "
                        "differ from the PASSED EP8 artifact's; v10 takes its "
                        "vectors from EP8 and requires them to agree")

    published_route = contract.get("routingGuard") or {}
    for key in ("vectorsDriven", "distinctIntentsDriven", "observedCalls",
                "depthZeroCalls", "distinctFingerprintsObserved",
                "supersededCallsInsideJoin"):
        _expect(published_route, key, heavy["routing"][key],
                "EP10-ROUTE: routingGuard", findings)
    if published_route.get("readsSource") is not False:
        findings.append("EP10-ROUTE: routingGuard.readsSource must be false; the "
                        "load-bearing guard may not be a source scan")
    if (contract.get("checkerModeContract") or {}).get(
            "exitMatrixIsObservedBehaviourally") is not True:
        findings.append("EP10-EXIT: checkerModeContract must declare the exit "
                        "matrix observed behaviourally")

    stability = heavy["stability"]
    published = contract.get("planIntentCommitmentStability") or {}
    if published.get("unmovedFromEP8") is not True:
        findings.append("EP10-COMMITMENT-MOVED: planIntentCommitmentStability."
                        "unmovedFromEP8 must be true and recomputed")
    for key in ("vectors", "recomputedUnderV4", "reproducedUnderSupersededEncoder",
                "preimageByteIdentical", "distinctCommitments",
                "preimageByteLengths", "distinctFrozenPlanIntents",
                "distinctPlanDescriptors"):
        _expect(published, key, stability[key],
                "EP10-STABILITY: planIntentCommitmentStability", findings)
    if "forced by the input" not in (published.get("whatThisDoesNotEstablish") or ""):
        findings.append("EP10-STABILITY: planIntentCommitmentStability must state "
                        "that a distinct-commitment count of 1 over one distinct "
                        "intent is FORCED BY THE INPUT, not established by the "
                        "measurement")

    # Non-circular: the declared commitment is compared against the digest-pinned
    # EP8 artifact's field AND required to be a member of THIS RUN's recomputed
    # set.  No literal in this checker's own text can make a candidate pass.
    ep8_commitment = (source_artifact.get("c2AuthorityJoin") or {}).get(
        "expectedPlanIntentCommitment")
    join = contract.get("c2AuthorityJoin") or {}
    if join.get("expectedPlanIntentCommitment") != ep8_commitment:
        findings.append("EP10-COMMITMENT-MOVED: c2AuthorityJoin."
                        "expectedPlanIntentCommitment differs from the digest-pinned "
                        "EP8 artifact's value")
    if join.get("expectedPlanIntentCommitment") not in \
            stability["distinctCommitments"]:
        findings.append("EP10-COMMITMENT-MOVED: the declared commitment is not a "
                        "member of the set this run recomputed through C-2 v4")

    family = heavy["family"]
    published_family = contract.get("distinctIntentFamily") or {}
    for key in ("declaredPerturbations", "acceptedByRepairedInstrument",
                "distinctIntentsDriven", "rejectedPerturbations",
                "distinctCommitments", "injective",
                "reproducedUnderSupersededEncoder", "preimageByteIdentical"):
        _expect(published_family, key, family[key],
                "EP10-FAMILY: distinctIntentFamily", findings)
    if not family["injective"]:
        findings.append("EP10-FAMILY: the repaired encoder did not map the distinct "
                        "PlanIntent family injectively onto distinct commitments")

    findings += verify_regimes(contract, heavy["regimeA"], heavy["regimeB"],
                               heavy["controls"])

    probe = heavy["probe"]
    published_probe = contract.get("lbC201ProbeFamily") or {}
    for key in ("cases", "repairedAdmitted", "supersededAdmitted", "secondDigests",
                "admitThenRaise", "discriminatingCardinality"):
        _expect(published_probe, key, probe[key],
                "EP10-PROBE: lbC201ProbeFamily", findings)
    if probe["repairedAdmitted"]:
        findings.append(f"EP10-PROBE: the repaired instrument admitted "
                        f"{probe['repairedAdmitted']} type-distinct case(s)")
    if probe["supersededAdmitted"] != probe["supersededAdmittedDerivedExpectation"]:
        findings.append("EP10-PROBE: the superseded control admitted "
                        f"{probe['supersededAdmitted']} cases where the injection "
                        "and leaf tables DERIVE "
                        f"{probe['supersededAdmittedDerivedExpectation']}; the "
                        "control has stopped modelling the defect")
    if published_probe.get("isTheGuard") is not False:
        findings.append("EP10-PROBE: lbC201ProbeFamily.isTheGuard must be false; "
                        "RET-EP10-03 retracts the claim that a fixed probe family "
                        "is the load-bearing guard")

    oracle = heavy["oracle"]
    published_oracle = contract.get("differentialOracle") or {}
    _expect(published_oracle, "executedCases", oracle["stats"]["executedCases"],
            "EP10-DIFF: differentialOracle", findings)
    _expect(published_oracle, "joinVsRepairedMismatches",
            oracle["stats"]["joinVsRepairedMismatches"],
            "EP10-DIFF: differentialOracle", findings)
    _expect(published_oracle, "discriminatingCardinality",
            oracle["discriminatingCardinality"], "EP10-DIFF: differentialOracle",
            findings)
    _expect(published_oracle, "discriminatingPositions", oracle["firstDivergent"],
            "EP10-DIFF: differentialOracle", findings)
    if published_oracle.get("isSufficientAlone") is not False:
        findings.append("EP10-DIFF: differentialOracle.isSufficientAlone must be "
                        "false; the evasion measurement shows the R1/R4 class "
                        "agrees with it everywhere")

    findings += verify_evasion(contract, heavy["evasion"])

    # The counterpart record lives on the AUTHORITY, and the dict stored in the
    # cache is the SAME object the nested checks read.  That matters: the
    # constant-leaf battery re-runs the complete checking layer once per injected
    # leaf, and if those nested runs could not see that a counterpart was
    # executing they would all fail for the wrong reason and the battery's
    # rejection count would be an artifact of the instrument rather than a
    # measurement of the candidate.
    counterparts = authority.cache.get("counterparts")
    if counterparts is None:
        counterparts = {}
        authority.cache["counterparts"] = counterparts
    counterparts["c2-route"] = heavy["evasion"]
    if not _NESTED[0]:
        matrix = exit_matrix_probe(contract, HERE / BINDING, authority, full=False)
        counterparts["selftest-dispatch"] = matrix
        for row in matrix:
            if not row["agrees"]:
                findings.append(f"EP10-EXIT: invocation {row['invocation']!r} "
                                f"returned {row['observed']}, expected "
                                f"{row['expected']}")
        counterparts["integer-guard"] = "EXECUTING"
        battery = own_constant_leaf_battery(contract, authority)
        counterparts["integer-guard"] = battery
        published_battery = (contract.get("astScanScope") or {}).get(
            "ownConstantLeafBattery") or {}
        for key in ("intBoolLeaves", "cases", "rejected", "silentlyAdmitted",
                    "silentlyAdmittedPositions"):
            _expect(published_battery, key, battery[key],
                    "EP10-BATTERY: ownConstantLeafBattery", findings)

    root_census, _paths = node_census(contract)
    findings += verify_scans(contract, heavy["evasion"], counterparts)
    findings += verify_totality(contract, heavy, root_census)

    authority.measurement = {**heavy, "contractRoot": root_census,
                             "counterparts": counterparts}
    return findings


# --------------------------------------------------------------------------
# Section 15.  Selftest and entrypoint.
# --------------------------------------------------------------------------

SELFTEST_MUTATIONS = (
    ("version is the JSON float 10.0", ("version",), 10.0),
    ("version is JSON true", ("version",), True),
    ("status silently applied", ("status",), "APPLIED"),
    ("reviewState pre-cleared", ("reviewState",), "REVIEWED"),
    ("sealRecommendation flipped", ("sealRecommendation",), "SEAL"),
    ("assurance state escalated", ("assurance", "state"), "QUALIFIED"),
    ("evidence grade escalated", ("assurance", "evidenceGrade"), "EXECUTED"),
    ("RET-EP10-01 softened into a scoping note",
     ("retractions", 0, "disposition"), "SCOPED"),
    ("RET-EP10-01 retracted text detached from the predecessor",
     ("retractions", 0, "retractedText"), "not a fragment of v9"),
    ("probe family reclaimed as the guard",
     ("lbC201ProbeFamily", "isTheGuard"), True),
    ("differential oracle claimed sufficient alone",
     ("differentialOracle", "isSufficientAlone"), True),
    ("AST scan reclaimed as a sole guard",
     ("astScanScope", "isSoleGuardForAnyProperty"), True),
    ("routing-scan blind spot denied",
     ("astScanScope", "routingScanCannotSeeWhichModuleServes"), False),
    ("regime-B admitted count understated",
     ("admittedClassMeasurement", "regimes", "B", "admittedCount"), 1),
    ("identity movement beneath an identical seal denied",
     ("admittedClassMeasurement", "identityMovingUnderByteIdenticalSeal"), 0),
    ("an admitted regime-B position deleted",
     ("admittedClassMeasurement", "regimes", "B", "admitted"), []),
    ("evasion blind spot understated",
     ("evasionMeasurement", "missedByAstTripwire"), 0),
    ("routing ledger catch count overstated",
     ("evasionMeasurement", "caughtByRoutingLedger"), 99),
    ("distinct intents overstated",
     ("planIntentCommitmentStability", "distinctFrozenPlanIntents"), 7),
    ("the 'forced by the input' disclosure deleted",
     ("planIntentCommitmentStability", "whatThisDoesNotEstablish"), "n/a"),
    ("contract-root census understated",
     ("scalarLeafTotality", "contractRoot", "scalarLeafPaths"), 1),
    ("a pinned digest edited",
     ("delegationClosure", "executables", 0, "sha256"), "0" * 64),
    ("the pin-agreement scope claim widened to 10/10",
     ("delegationClosure", "pinAgreementRule"),
     "every predecessor's own declared pin table is cross-checked"),
    ("the RES-EP10-01 residual deleted",
     ("c2AuthorityRepairJoin", "ep6InnerJoinResidual"), "closed"),
)


def selftest(contract, authority, path) -> int:
    base = check(contract, authority)
    if base:
        print("SELFTEST-REFUSED: the base candidate is already dirty; a mutation "
              "suite over a dirty base proves nothing")
        for item in base[:5]:
            print("  -", item)
        print(f"SELFTEST-NOT-RUN: 0 of {len(SELFTEST_MUTATIONS)} mutations executed")
        return 3

    print(f"EP10 SELFTEST — {path.name}")
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
            findings = check(mutated, authority)
        finally:
            _NESTED[0] -= 1
        if findings:
            print(f"  reject  {label}")
            print(f"            -> {findings[0][:140]}")
        else:
            escaped.append(label)
            print(f"  ESCAPE  {label}")

    print()
    matrix = exit_matrix_probe(contract, path, authority, full=True)
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
    print("  evasion battery, re-stated from this run:")
    for row in evasion["rows"]:
        print(f"    {row['variant']}: astTripwire="
              f"{row.get('caughtByAstTripwire')}, differentialOracle="
              f"{row.get('caughtByDifferentialOracle')}, routingLedger="
              f"{row.get('caughtByRoutingLedger')}")
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
    print("  RES-EP10-01: v10 does NOT repair check-evaluation-proof-v6.py; EP6's "
          "inner C-2 join still runs against the DEFECTIVE check-c2.py bytes")
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
        print(f"EP10-UNSUPPORTED-INVOCATION: {exc}", file=sys.stderr)
        return 2
    try:
        if override and override.get("authority") is not None:
            authority = override["authority"]
        else:
            authority = load_authority()
    except AuthorityLoadError as exc:
        print(f"EP10-PINNED-INPUT-REFUSED: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2
    path = pathlib.Path(requested) if requested is not None else HERE / BINDING
    try:
        text = override["candidateText"] if override and "candidateText" in override \
            else path.read_text()
        contract = json.loads(text, object_pairs_hook=_pairs)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        print(f"cannot load the EP10 candidate {path}: {type(exc).__name__}: {exc}",
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
    print_banner(contract, authority, path)
    return 0


def print_banner(contract, authority, path) -> None:
    measurement = authority.measurement
    route = measurement["routing"]
    stability = measurement["stability"]
    family = measurement["family"]
    regime_a, regime_b = measurement["regimeA"], measurement["regimeB"]
    probe, evasion, oracle = (measurement["probe"], measurement["evasion"],
                              measurement["oracle"])
    root = measurement["contractRoot"]
    moving = [row for row in regime_b["admitted"]
              if row["classification"] == "type-distinct-one" and
              row["movedIdentities"]]
    under_seal = [row for row in moving
                  if "evaluationAuthoritySealRef" not in row["movedIdentities"]]
    descriptor = measurement["planDescriptorSurface"]

    print(f"EP10 contract OK — {path.name}")
    print(f"  delegation closure: {len(DELEGATION_CLOSURE)} executables + "
          f"{len(PINNED_DATA)} pinned data inputs + 1 superseded independent "
          "encoder, each read ONCE, SHA-256 verified, then executed or parsed from "
          "that verified byte string; every one recorded by filename and digest")
    print(f"  C-2 join RE-PINNED onto {C2V4_CONTRACT} / {C2V4}")
    print(f"  ROUTING ESTABLISHED BEHAVIOURALLY: {route['observedCalls']} C-2 calls "
          f"observed PER CALL across {route['vectorsDriven']} pinned vectors; "
          f"{route['distinctFingerprintsObserved']} distinct PlanIntent "
          f"fingerprint(s) bound to those calls; "
          f"{route['supersededCallsInsideJoin']} served by the superseded module "
          "(REQUIRED zero)")
    print(f"  evasion battery: {evasion['sourceVariantsBuilt']} source variants + "
          f"{evasion['objectAttacksBuilt']} object attacks BUILT AND EXECUTED. AST "
          f"tripwire caught {evasion['caughtByAstTripwire']}, MISSED "
          f"{evasion['missedByAstTripwire']}. Differential oracle caught "
          f"{evasion['caughtByDifferentialOracle']}, MISSED "
          f"{evasion['missedByDifferentialOracle']} — including the reviewer's R1 "
          f"and R4. Served-module ledger caught {evasion['caughtByRoutingLedger']} "
          f"of {evasion['variantsBuilt']}")
    print("  RET-EP10-01: v9's 'moves NO proof identity' mitigation is RETRACTED AS "
          f"FALSE. Under producer consistency {len(moving)} type-distinct-one "
          f"position(s) MOVE durable identity; {len(under_seal)} of them do so "
          "beneath a BYTE-IDENTICAL EvaluationAuthoritySealRef, and every one "
          "cold-reconstructs with assert_store_continuity() true")
    print(f"  admitted set RE-DERIVED BY EXECUTION, per regime: regime A "
          f"{regime_a['executedCases']} cases over {regime_a['scalarLeafPaths']} "
          f"scalar leaves -> {regime_a['admittedCount']} admitted, "
          f"{sum(1 for r in regime_a['admitted'] if r['movedIdentities'])} moving "
          f"identity; regime B (producer-consistent) {regime_b['executedCases']} "
          f"cases over {regime_b['scalarLeafPaths']} scalar leaves -> "
          f"{regime_b['admittedCount']} admitted, {len(moving)} moving identity. "
          "Every published position states its regime")
    print(f"  planIntentCommitment UNMOVED: {stability['vectors']} vectors carrying "
          f"{stability['distinctFrozenPlanIntents']} DISTINCT PlanIntent and "
          f"{stability['distinctPlanDescriptors']} distinct PlanDescriptor — a "
          f"distinct-commitment count of {len(stability['distinctCommitments'])} "
          "over that input is FORCED, not established (RET-EP10-04)")
    print("  the measurement that DOES discriminate: "
          f"{family['distinctIntentsDriven']} legally distinct PlanIntents, "
          f"{family['distinctCommitments']} distinct commitments, injective="
          f"{family['injective']}, {family['reproducedUnderSupersededEncoder']} "
          f"reproduced and {family['preimageByteIdentical']} byte-identical under "
          "the superseded encoder")
    print(f"  differential oracle (RETAINED, NOT SUFFICIENT ALONE): "
          f"{oracle['stats']['executedCases']} executed cases, "
          f"{oracle['stats']['joinVsRepairedMismatches']} join-vs-repaired "
          f"mismatches, measured discriminating cardinality "
          f"{oracle['discriminatingCardinality']}")
    print(f"  LB-C2-01 probe family (CONTROL ONLY, NOT the guard): {probe['cases']} "
          f"cases; repaired admitted {probe['repairedAdmitted']}; superseded "
          f"admitted {probe['supersededAdmitted']} ({probe['secondDigests']} second "
          f"digests, {probe['admitThenRaise']} admit-then-raise); measured "
          f"discriminating cardinality {probe['discriminatingCardinality']}")
    print("  hostile parsed JSON at EVERY position including scalar leaves: "
          f"{oracle['stats']['executedCases'] + descriptor['stats']['executedCases']} "
          f"executed cases over "
          f"{oracle['census']['enumeratedPaths'] + descriptor['census']['enumeratedPaths']} "
          "enumerated wire-surface paths of which "
          f"{oracle['census']['scalarLeafPaths'] + descriptor['census']['scalarLeafPaths']} "
          "are scalar leaves; 0 guarded escapes")
    print(f"  contract-root space measured at {root['enumeratedPaths']} paths of "
          f"which {root['scalarLeafPaths']} are scalar leaves")
    print("  RES-EP10-01: v10 does NOT repair check-evaluation-proof-v6.py; EP6's "
          "inner C-2 join still runs against the DEFECTIVE check-c2.py bytes "
          "underneath EP8, and v10 is a strictly stronger OUTER gate over it, not a "
          "replacement of its internals")
    print("  RES-EP10-03: a routing evasion produces no wrong ANSWER on today's "
          "pinned bytes (the reviewer's 2548-case differential fuzz found v3/v4 "
          "diverge at exactly the 4 LB-C2-01 pairs). The defect the ledger closes "
          "is in the EVIDENCE, not currently in the verdict")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED / "
          "AWAITING-INDEPENDENT-REVIEW; DO-NOT-SEAL; CD-RT-5 unsigned; independent "
          "re-review REQUIRED")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
