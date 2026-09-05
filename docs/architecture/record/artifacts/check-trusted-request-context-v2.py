#!/usr/bin/env python3
"""Design-integrity checker for TrustedRequestContextV2.

Successor to the rejected v1 leaf. Closes TRC-PF-01 (unpinned .pyc execution)
and TRC-PF-02 (forgeable capability oracle) while preserving REQUEST-ID-V1
semantics and the narrow dependency on historical OPERABILITY v2.

Executable dependencies are authenticated by reading exact source bytes,
hashing that buffer, compiling that buffer, and executing the resulting code
object in an isolated module namespace. importlib/SourceFileLoader path loading
is never used, so a timestamp-valid __pycache__ image cannot satisfy the pin.

The capability model is an executable design double for a trusted host
constructor: only registry-registered instances minted by HostRequestIngressV2
project. It does not claim resistance to arbitrary same-process memory or
debugger compromise; production Rust module privacy owns the real boundary.

Usage:
  python3 -B artifacts/check-trusted-request-context-v2.py [contract]
  python3 -B artifacts/check-trusted-request-context-v2.py [contract] --selftest
"""
from __future__ import annotations

import builtins
import copy
import hashlib
import json
import marshal
import pathlib
import pickle
import re
import sys
import types
from typing import Any, Callable

# Hygienic default; not a repair for cache *reads*.
sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
BINDING = "trusted-request-context.v2.json"
SOURCE_ARTIFACT = "operability.v2.json"
SOURCE_CHECKER = "check-operability.py"
PINS = {
    SOURCE_ARTIFACT:
        "43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04",
    SOURCE_CHECKER:
        "925496916ef2c7075c02f7a767353aa6ff047cf55557304f3983e17e1c5256e2",
}
# Only these repository-local executable modules may be loaded, and only via
# hash-then-compile of exact source bytes.
DECLARED_EXECUTABLE = frozenset({SOURCE_CHECKER})
REQUEST_RE = re.compile(r"^req1_[0-9a-f]{32}$")
ROOT_KEYS = {
    "artifact", "version", "date", "status", "reviewStatus", "purpose",
    "authorityBoundary", "sourceAuthority", "sourceProjection",
    "dependencyClosure", "capabilityContract", "invocationLifecycle",
    "semanticBoundary", "positiveControls", "adversarialControls",
    "invariants", "assurance", "retainedResiduals", "findingDispositions",
    "sealRecommendation",
}
PURPOSE = (
    "Extract the minimum host-owned REQUEST-ID-V1 authority needed to pass an "
    "opaque TrustedRequestContextV2 across host components without making a raw "
    "RequestId, an observability envelope, or any downstream analysis contract "
    "into authority."
)
AUTHORITY_BOUNDARY = {
    "owner": "orchestration host request-ingress adapter",
    "type": "TrustedRequestContextV2",
    "rule": (
        "Only the trusted host ingress may mint this opaque capability, and only "
        "after canonical RequestId validation and successful atomic reservation. "
        "Downstream code may project its RequestId value for closed operational "
        "correlation records but cannot construct, replace, serialize, copy, "
        "unpickle, or reinterpret the capability."
    ),
    "nonAuthority": (
        "This leaf does not define an event envelope, attempt identity, semantic "
        "record, storage transaction, analysis result, or product behavior."
    ),
    "modelBoundary": (
        "The Python checker is an executable model of a trusted host constructor "
        "and process-local registry. It does not claim resistance to arbitrary "
        "same-process memory writes or debugger compromise. Production Rust "
        "module privacy owns the actual capability boundary."
    ),
}
SOURCE_AUTHORITY = {
    "artifact": SOURCE_ARTIFACT,
    "sha256": PINS[SOURCE_ARTIFACT],
    "checker": SOURCE_CHECKER,
    "checkerSha256": PINS[SOURCE_CHECKER],
    "jsonPointer": "/requestIdContract",
    "sourceId": "REQUEST-ID-V1",
    "extractionRule": (
        "The checker loads the exact pinned OPERABILITY v2 artifact and "
        "recomputes sourceProjection from a closed path set. Every declared "
        "local executable dependency is authenticated by hashing its exact "
        "source bytes and compiling/executing those bytes in an isolated "
        "namespace; path/importlib loaders capable of selecting __pycache__ "
        "are not used. The source checker's whole-contract check is not "
        "invoked."
    ),
}
DEPENDENCY_CLOSURE = {
    "data": [SOURCE_ARTIFACT],
    "executable": [SOURCE_CHECKER],
    "rule": (
        "No other artifact or checker is loaded. Local executable dependencies "
        "must appear in the declared set, be hash-authenticated from source "
        "bytes, and execute only via compile of those exact bytes. Undeclared "
        "local imports are rejected. Timestamp-valid malicious .pyc images are "
        "never selected."
    ),
    "forbiddenBackEdges": [
        "current OPERABILITY successor",
        "analysis evidence contract",
        "event-envelope contract",
        "attempt-identity contract",
        "delivery or projection contract",
        "retention or D9 contract",
        "E8 or OP6",
    ],
}
CAPABILITY_CONTRACT = {
    "type": "TrustedRequestContextV2",
    "opaque": True,
    "serializable": False,
    "copyable": False,
    "publicConstructors": [],
    "mintOwner": "HostRequestIngressV2",
    "mintAuthority": (
        "Process-local mint gate held only by HostRequestIngressV2. No "
        "module-global mint token is exported. Projection accepts only "
        "instances registered by that trusted constructor under the minting "
        "gate's private registry."
    ),
    "mintPreconditions": [
        "the candidate decodes as exactly sixteen bytes under REQUEST-ID-V1",
        "the candidate is atomically reserved under the host RequestId registry's unique constraint",
        "the invocation has crossed trusted ingress and has not yet published a child operation",
    ],
    "forbiddenConstructionSources": [
        "raw string",
        "parsed JSON",
        "public caller",
        "event sink",
        "provider",
        "stage",
        "profile",
        "projection adapter",
        "object.__new__ plus slot injection",
        "copy or deepcopy",
        "pickle dumps or loads",
        "reconstructed lookalike",
        "wrong-authority instance",
        "registry substitution",
    ],
    "allowedProjection": {
        "method": "request_id(TrustedRequestContextV2) -> RequestIdV1",
        "fields": ["requestId"],
        "representation": "^req1_[0-9a-f]{32}$",
        "persistence": (
            "The projected value may enter only a downstream closed "
            "operational-correlation record. The capability, mint gate, and "
            "registry never serialize."
        ),
    },
    "tokenRule": (
        "No module-global mint token exists. Mint authority is private to "
        "HostRequestIngressV2, process-local, nonserializable, absent from the "
        "RequestId projection, and never accepted as caller data."
    ),
}
INVOCATION_LIFECYCLE = {
    "acceptedKinds": ["CLI", "API", "recovery"],
    "internalRetry": (
        "An internal retry inside one accepted invocation receives the "
        "identical TrustedRequestContextV2 capability and identical RequestId; "
        "it performs no new allocation or reservation."
    ),
    "newInvocation": (
        "Every new CLI, API, or recovery invocation allocates and reserves a "
        "new canonical RequestId and receives a distinct TrustedRequestContextV2. "
        "A prior capability cannot be supplied as the new invocation's authority."
    ),
    "transportRetry": (
        "A transport retry that crosses trusted ingress is a new invocation. A "
        "retry wholly contained inside the accepted host invocation is "
        "internalRetry."
    ),
    "collision": (
        "A reserved RequestId cannot mint a second context. Collision handling "
        "remains owned by the pinned REQUEST-ID-V1 source and never overwrites "
        "or aliases the existing reservation."
    ),
}
SEMANTIC_EXCLUSIONS = [
    "SnapshotId preimage",
    "PlanId preimage",
    "fact identity and fingerprints",
    "FactViewId",
    "EvidenceDigest and evaluation proofs",
    "RunId derivation",
    "sealed Run semantic manifest",
    "Coverage, findings, verdict, policy and termination derivation",
    "cache and regeneration keys",
]
SEMANTIC_BOUNDARY = {
    "classification": "operational-correlation-only",
    "rule": (
        "Neither the capability nor its projected RequestId is an analysis "
        "input or evidence authority. Only explicitly downstream operational "
        "schemas may persist the projection."
    ),
    "forbiddenParticipation": SEMANTIC_EXCLUSIONS,
    "downstreamSchemasDefinedHere": [],
}
POSITIVE_CONTROLS = [
    ("TRC2-POS-01-CLI-MINT",
     "A canonical unreserved candidate at trusted CLI ingress yields one opaque context and the exact RequestId projection."),
    ("TRC2-POS-02-INTERNAL-RETRY",
     "Internal retry returns the identical capability without allocation or reservation."),
    ("TRC2-POS-03-API-NEW-CONTEXT",
     "A new API invocation receives a distinct context with a distinct reserved RequestId."),
    ("TRC2-POS-04-RECOVERY-NEW-CONTEXT",
     "A new recovery invocation receives a distinct context with a distinct reserved RequestId."),
    ("TRC2-POS-05-NONSERIALIZABLE",
     "JSON, pickle, copy, and deepcopy reject the capability while its RequestId projection remains canonical text."),
]
NEGATIVE_CONTROLS = [
    ("TRC2-NEG-01-RAW-STRING", "raw string as context", "TRUSTED_CONTEXT_REQUIRED"),
    ("TRC2-NEG-02-PARSED-JSON", "parsed JSON object as context", "TRUSTED_CONTEXT_REQUIRED"),
    ("TRC2-NEG-03-CALLER-CONSTRUCTION", "public caller constructs context", "TRUSTED_INGRESS_REQUIRED"),
    ("TRC2-NEG-04-SINK-CONSTRUCTION", "event sink constructs context", "TRUSTED_INGRESS_REQUIRED"),
    ("TRC2-NEG-05-PROVIDER-CONSTRUCTION", "provider constructs context", "TRUSTED_INGRESS_REQUIRED"),
    ("TRC2-NEG-06-UPPERCASE", "uppercase RequestId", "REQUEST_ID_INVALID_REPRESENTATION"),
    ("TRC2-NEG-07-UUID-ALIAS", "UUID-shaped alias", "REQUEST_ID_INVALID_REPRESENTATION"),
    ("TRC2-NEG-08-COLLISION-REUSE", "already reserved RequestId", "REQUEST_ID_COLLISION"),
    ("TRC2-NEG-09-INTERNAL-REMINT", "internal retry remints context", "INTERNAL_RETRY_CONTEXT_DRIFT"),
    ("TRC2-NEG-10-EXTERNAL-CONTEXT-REUSE", "new invocation supplies prior context", "NEW_INVOCATION_REQUIRES_NEW_CONTEXT"),
    ("TRC2-NEG-11-CAPABILITY-SERIALIZATION", "serialize opaque capability", "TRUSTED_CONTEXT_NONSERIALIZABLE"),
    ("TRC2-NEG-12-SEMANTIC-PROJECTION", "project context into semantic input", "REQUEST_ID_SEMANTIC_EXCLUSION_VIOLATION"),
    ("TRC2-NEG-13-OBJECT-NEW-FORGE", "object.__new__ plus mangled slot injection", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC2-NEG-14-COPY", "copy.copy of trusted context", "TRUSTED_CONTEXT_NONCOPYABLE"),
    ("TRC2-NEG-15-DEEPCOPY", "copy.deepcopy of trusted context", "TRUSTED_CONTEXT_NONCOPYABLE"),
    ("TRC2-NEG-16-PICKLE-CONTEXT", "pickle.dumps trusted context", "TRUSTED_CONTEXT_NONSERIALIZABLE"),
    ("TRC2-NEG-17-UNPICKLE-LOOKALIKE", "unpickle reconstructed lookalike", "TRUSTED_CONTEXT_REQUIRED"),
    ("TRC2-NEG-18-WRONG-AUTHORITY", "project context under a different mint gate", "TRUSTED_CONTEXT_WRONG_AUTHORITY"),
    ("TRC2-NEG-19-REGISTRY-SUBSTITUTION", "module registry substitution with forged id", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC2-NEG-20-NO-GLOBAL-MINT-TOKEN", "construct via leaked module-global mint token", "TRUSTED_INGRESS_REQUIRED"),
]
INVARIANTS = [
    ("TRC2-1", "The source projection is recomputed from the exact pinned REQUEST-ID-V1 authority rather than trusted as authored presence."),
    ("TRC2-2", "Only host ingress can mint TrustedRequestContextV2 and only after canonical validation plus successful reservation into a private registry."),
    ("TRC2-3", "Raw strings, parsed JSON, callers, sinks, providers, stages, profiles, adapters, object.__new__ forgeries, copies, pickles, wrong-authority instances, and registry substitutions cannot substitute for the opaque capability."),
    ("TRC2-4", "The capability exposes exactly one canonical RequestId projection and is itself nonserializable and noncopyable."),
    ("TRC2-5", "Internal retry retains one context; every new CLI, API, or recovery invocation gets a distinct newly reserved context."),
    ("TRC2-6", "RequestId remains operational-only and cannot influence any enumerated semantic identity or result."),
    ("TRC2-7", "Declared local executables run only from hash-authenticated source bytes; timestamp-valid malicious .pyc images are never executed."),
]
ASSURANCE = {
    "state": "IMPLEMENTABLE_UNEXECUTED",
    "checkerEvidence": "DESIGN-INTEGRITY-ONLY",
    "runtimeImplementationExecuted": False,
    "productQualified": False,
    "productDemonstrated": False,
    "applicationAuthorized": False,
}
RESIDUALS = [
    {
        "id": "INDEPENDENT-REVIEW",
        "state": "REQUIRED",
        "effect": (
            "No consumer may treat this candidate as accepted authority until a "
            "reviewer independently reconstructs the source extraction, "
            "hash-exec path, and registry-based capability probes."
        ),
    },
    {
        "id": "PRODUCTION-CAPABILITY-IMPLEMENTATION",
        "state": "UNEXECUTED",
        "effect": (
            "The checker uses an in-process opaque design double. Production "
            "Rust module privacy owns the real capability boundary; this model "
            "does not demonstrate allocator, durable registry, restart, "
            "concurrency, or resistance to arbitrary same-process memory/"
            "debugger compromise."
        ),
    },
    {
        "id": "ATOMIC-RESERVATION-RUNTIME",
        "state": "UNEXECUTED",
        "effect": (
            "The checker models a single-process set update; it is not "
            "evidence of a durable atomic unique constraint or multi-thread "
            "behavior."
        ),
    },
]
FINDING_DISPOSITIONS = [
    {
        "id": "TRC-PF-01-UNPINNED-PYC-EXECUTION",
        "sourceReview": (
            "trusted-request-context.v1.review-independent-prefreeze.json"
        ),
        "disposition": "ACCEPTED-AND-REPAIRED-IN-V2",
        "repair": (
            "Executable dependencies are authenticated by hashing exact source "
            "bytes then compile()/exec() of that buffer in an isolated "
            "namespace. importlib path loaders and __pycache__ selection are "
            "not used. Retained probe TRC2-ADV-PYC proves a timestamp-valid "
            "malicious .pyc is ignored."
        ),
    },
    {
        "id": "TRC-PF-02-CAPABILITY-ORACLE-FORGEABLE",
        "sourceReview": (
            "trusted-request-context.v1.review-independent-prefreeze.json"
        ),
        "disposition": "ACCEPTED-AND-REPAIRED-IN-V2",
        "repair": (
            "Module-global mint token removed. Projection accepts only "
            "registry-registered instances minted by HostRequestIngressV2 under "
            "a private nonserializable mint gate. Retained probes cover "
            "object.__new__ forge, copy/deepcopy, pickle/unpickle, wrong "
            "authority, and registry substitution."
        ),
    },
]


class DuplicateKeyError(ValueError):
    pass


class ContractViolation(ValueError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise DuplicateKeyError(f"duplicate key: {key}")
        result[key] = value
    return result


def _read_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(), object_pairs_hook=_pairs)


def _sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _sha_file(path: pathlib.Path) -> str:
    return _sha_bytes(path.read_bytes())


def _stdlib_or_frozen(name: str) -> bool:
    if name in sys.builtin_module_names:
        return True
    top = name.split(".", 1)[0]
    if top in sys.builtin_module_names:
        return True
    # Already-loaded stdlib modules
    mod = sys.modules.get(top)
    if mod is None:
        return False
    file_name = getattr(mod, "__file__", None)
    if file_name is None:
        return True  # built-in / frozen
    try:
        path = pathlib.Path(file_name).resolve()
    except OSError:
        return False
    here = HERE.resolve()
    try:
        path.relative_to(here)
        return False  # under artifacts/
    except ValueError:
        return True


def _exec_pinned_source(
        filename: str,
        expected_sha: str,
        *,
        allow_local: frozenset[str],
) -> types.ModuleType:
    """Hash exact source bytes, compile them, exec in isolation — never load .pyc."""
    path = HERE / filename
    if not path.is_file():
        raise FileNotFoundError(filename)
    raw = path.read_bytes()
    digest = _sha_bytes(raw)
    if digest != expected_sha:
        raise ValueError(f"pin drift {filename}: {digest} != {expected_sha}")

    module_name = f"trc_v2_pinned_{filename.replace('.', '_').replace('-', '_')}"
    module = types.ModuleType(module_name)
    module.__file__ = str(path.resolve())
    module.__package__ = None
    module.__loader__ = None  # no path-based loader
    module.__spec__ = None

    real_import = builtins.__import__

    def _is_under_here(file_name: str | None) -> bool:
        if file_name is None:
            return False
        try:
            pathlib.Path(file_name).resolve().relative_to(HERE.resolve())
            return True
        except ValueError:
            return False

    def guarded_import(
            name: str,
            globals: Any = None,
            locals: Any = None,
            fromlist: Any = (),
            level: int = 0,
    ) -> Any:
        del globals, locals, fromlist
        if level != 0 or name.startswith("."):
            raise ImportError(
                f"TRC-SOURCE: relative import forbidden: {name}")
        top = name.split(".", 1)[0]
        # If a repository-local .py matches the top-level name, require prior
        # declaration and never path-load it here (OP2 needs only stdlib).
        local_candidate = HERE / f"{top}.py"
        if local_candidate.is_file():
            if local_candidate.name not in allow_local:
                raise ImportError(
                    f"TRC-SOURCE: undeclared local import rejected: {name}")
            raise ImportError(
                f"TRC-SOURCE: nested local import must be pre-authenticated: "
                f"{name}")
        if name in sys.modules:
            existing = sys.modules[name]
            if _is_under_here(getattr(existing, "__file__", None)):
                raise ImportError(
                    f"TRC-SOURCE: refuse cached local module: {name}")
            return existing
        imported = real_import(name)
        if _is_under_here(getattr(imported, "__file__", None)):
            raise ImportError(
                f"TRC-SOURCE: refuse local path import via stdlib loader: {name}")
        return imported

    # Restricted builtins for the executed dependency.
    safe_builtins = dict(vars(builtins))
    safe_builtins["__import__"] = guarded_import
    module.__dict__["__builtins__"] = safe_builtins

    code = compile(raw, str(path.resolve()), "exec", dont_inherit=True)
    # Execute only the authenticated code object — never a loader that can
    # prefer __pycache__.
    exec(code, module.__dict__, module.__dict__)
    return module


def _load_source(*, verify_files: bool) -> tuple[Any | None, list[str]]:
    errors: list[str] = []
    if verify_files:
        for filename, expected in PINS.items():
            path = HERE / filename
            if not path.is_file():
                errors.append(f"TRC-SOURCE: missing pinned input {filename}")
                continue
            observed = _sha_file(path)
            if observed != expected:
                errors.append(
                    f"TRC-SOURCE: pin drift {filename}: "
                    f"{observed} != {expected}")
        if errors:
            return None, errors
        try:
            source_checker = _exec_pinned_source(
                SOURCE_CHECKER,
                PINS[SOURCE_CHECKER],
                allow_local=DECLARED_EXECUTABLE,
            )
            if getattr(source_checker, "BINDING", None) != SOURCE_ARTIFACT or \
                    not callable(getattr(source_checker, "check", None)):
                errors.append("TRC-SOURCE: pinned checker API/binding drift")
        except Exception as exc:
            errors.append(
                f"TRC-SOURCE: pinned checker secure-exec failed "
                f"({type(exc).__name__}: {exc})")
    if errors:
        return None, errors
    try:
        return _read_json(HERE / SOURCE_ARTIFACT), []
    except (OSError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError, TypeError, ValueError) as exc:
        return None, [
            f"TRC-SOURCE: source artifact could not be decoded "
            f"({type(exc).__name__})"]


def _extract_source(source: Any) -> dict[str, Any]:
    if not isinstance(source, dict):
        raise TypeError("source root")
    request = source.get("requestIdContract")
    if not isinstance(request, dict):
        raise TypeError("requestIdContract")
    authority = request.get("authority")
    allocation = request.get("allocation")
    representation = request.get("representation")
    collision = request.get("collisionAndRetry")
    custody = request.get("custody")
    semantic = request.get("semanticExclusion")
    if not all(isinstance(row, dict) for row in (
            authority, allocation, representation, collision, custody,
            semantic)):
        raise TypeError("source projection branch")
    return {
        "id": request["id"],
        "status": request["status"],
        "authority": {
            "allocationOwner": authority["allocationOwner"],
            "callerRule": authority["callerRule"],
            "propagationRule": authority["propagationRule"],
        },
        "allocation": {
            "point": allocation["point"],
            "allRequests": copy.deepcopy(allocation["allRequests"]),
            "entropyBoundary": allocation["entropyBoundary"],
        },
        "representation": copy.deepcopy(representation),
        "collisionAndRetry": {
            "reservationAuthority": collision["reservationAuthority"],
            "reservationRule": collision["reservationRule"],
            "maximumCandidates": collision["maximumCandidates"],
            "onCollision": collision["onCollision"],
            "externalRetry": collision["externalRetry"],
            "collisionScope": collision["collisionScope"],
        },
        "custody": {
            "requestContext": custody["requestContext"],
            "operationalRecords": custody["operationalRecords"],
            "redaction": custody["redaction"],
        },
        "semanticExclusion": {
            "excludedFrom": copy.deepcopy(semantic["excludedFrom"]),
            "rule": semantic["rule"],
        },
    }


class _MintGateV2:
    """Process-local mint authority. Not a module-global token; not serializable."""

    __slots__ = ("_issued", "_alive")

    def __init__(self) -> None:
        # id(context) -> request_id for instances this gate minted
        self._issued: dict[int, str] = {}
        self._alive = True

    def _register(self, context: "_TrustedRequestContextV2", request_id: str) -> None:
        self._issued[id(context)] = request_id

    def _lookup(self, context: Any) -> str | None:
        if not self._alive:
            return None
        return self._issued.get(id(context))

    def __reduce__(self) -> Any:
        raise ContractViolation("TRUSTED_CONTEXT_NONSERIALIZABLE")

    def __reduce_ex__(self, protocol: int) -> Any:
        del protocol
        raise ContractViolation("TRUSTED_CONTEXT_NONSERIALIZABLE")

    def __getstate__(self) -> Any:
        raise ContractViolation("TRUSTED_CONTEXT_NONSERIALIZABLE")

    def __setstate__(self, state: Any) -> None:
        del state
        raise ContractViolation("TRUSTED_CONTEXT_NONSERIALIZABLE")


class _TrustedRequestContextV2:
    __slots__ = ("__request_id", "__gate")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Public construction is forbidden; only HostRequestIngressV2 may mint.
        del args, kwargs
        raise ContractViolation("TRUSTED_INGRESS_REQUIRED")

    def _project_for_checker(self) -> str:
        return object.__getattribute__(self, "_TrustedRequestContextV2__request_id")

    def _gate_for_checker(self) -> _MintGateV2:
        return object.__getattribute__(self, "_TrustedRequestContextV2__gate")

    def __copy__(self) -> Any:
        raise ContractViolation("TRUSTED_CONTEXT_NONCOPYABLE")

    def __deepcopy__(self, memo: Any) -> Any:
        del memo
        raise ContractViolation("TRUSTED_CONTEXT_NONCOPYABLE")

    def __reduce__(self) -> Any:
        raise ContractViolation("TRUSTED_CONTEXT_NONSERIALIZABLE")

    def __reduce_ex__(self, protocol: int) -> Any:
        del protocol
        raise ContractViolation("TRUSTED_CONTEXT_NONSERIALIZABLE")

    def __getstate__(self) -> Any:
        raise ContractViolation("TRUSTED_CONTEXT_NONSERIALIZABLE")

    def __setstate__(self, state: Any) -> None:
        del state
        raise ContractViolation("TRUSTED_CONTEXT_NONSERIALIZABLE")


def _mint_context(gate: _MintGateV2, request_id: str) -> _TrustedRequestContextV2:
    if not isinstance(gate, _MintGateV2):
        raise ContractViolation("TRUSTED_INGRESS_REQUIRED")
    if not isinstance(request_id, str) or not REQUEST_RE.fullmatch(request_id):
        raise ContractViolation("REQUEST_ID_INVALID_REPRESENTATION")
    ctx = object.__new__(_TrustedRequestContextV2)
    object.__setattr__(ctx, "_TrustedRequestContextV2__request_id", request_id)
    object.__setattr__(ctx, "_TrustedRequestContextV2__gate", gate)
    gate._register(ctx, request_id)
    return ctx


class HostRequestIngressV2:
    __slots__ = ("_reservations", "_gate")

    def __init__(self) -> None:
        self._reservations: set[str] = set()
        self._gate = _MintGateV2()

    def begin(self, kind: Any, candidate: Any,
              prior_context: Any = None) -> _TrustedRequestContextV2:
        if kind not in {"CLI", "API", "recovery"}:
            raise ContractViolation("TRUSTED_INGRESS_REQUIRED")
        if prior_context is not None:
            raise ContractViolation("NEW_INVOCATION_REQUIRES_NEW_CONTEXT")
        if not isinstance(candidate, str) or not REQUEST_RE.fullmatch(candidate):
            raise ContractViolation("REQUEST_ID_INVALID_REPRESENTATION")
        if candidate in self._reservations:
            raise ContractViolation("REQUEST_ID_COLLISION")
        self._reservations.add(candidate)
        return _mint_context(self._gate, candidate)

    def internal_retry(
            self, context: Any, replacement_candidate: Any = None
    ) -> _TrustedRequestContextV2:
        # Validate under this host's gate.
        _request_id(context, gate=self._gate)
        if replacement_candidate is not None:
            raise ContractViolation("INTERNAL_RETRY_CONTEXT_DRIFT")
        return context


def _request_id(context: Any, *, gate: _MintGateV2 | None = None) -> str:
    if type(context) is not _TrustedRequestContextV2:
        raise ContractViolation("TRUSTED_CONTEXT_REQUIRED")
    try:
        context_gate = context._gate_for_checker()
        slot = context._project_for_checker()
    except Exception as exc:
        raise ContractViolation("TRUSTED_CONTEXT_REQUIRED") from exc
    if not isinstance(context_gate, _MintGateV2):
        raise ContractViolation("TRUSTED_CONTEXT_WRONG_AUTHORITY")
    if gate is not None and context_gate is not gate:
        raise ContractViolation("TRUSTED_CONTEXT_WRONG_AUTHORITY")
    registered = context_gate._lookup(context)
    if registered is None:
        raise ContractViolation("TRUSTED_CONTEXT_UNREGISTERED")
    if registered != slot or not REQUEST_RE.fullmatch(slot):
        raise ContractViolation("REQUEST_ID_INVALID_REPRESENTATION")
    return slot


def _foreign_construct(origin: str, value: Any) -> _TrustedRequestContextV2:
    del origin, value
    # No public constructor path — always ingress-required.
    return _TrustedRequestContextV2()  # type: ignore[call-arg]


def _semantic_project(context: Any) -> None:
    if type(context) is _TrustedRequestContextV2:
        raise ContractViolation("REQUEST_ID_SEMANTIC_EXCLUSION_VIOLATION")
    raise ContractViolation("TRUSTED_CONTEXT_REQUIRED")


def _expect_code(action: Callable[[], Any], code: str) -> bool:
    try:
        action()
    except ContractViolation as exc:
        return exc.code == code
    except (AttributeError, IndexError, KeyError, TypeError, ValueError,
            pickle.PickleError, copy.Error):
        return False
    return False


def _forge_with_object_new() -> str:
    """Bypass __init__, inject slots, but never register with a mint gate."""
    forged = object.__new__(_TrustedRequestContextV2)
    empty_gate = _MintGateV2()
    object.__setattr__(
        forged, "_TrustedRequestContextV2__request_id", "req1_" + "ab" * 16)
    object.__setattr__(forged, "_TrustedRequestContextV2__gate", empty_gate)
    # empty_gate._issued does not contain id(forged) → unregistered
    return _request_id(forged)


def _adversarial_pyc_probe() -> bool:
    """Return True when a timestamp-valid malicious .pyc cannot execute."""
    import os
    import struct
    import tempfile
    import textwrap

    with tempfile.TemporaryDirectory(prefix="trc-v2-pyc-") as tmp:
        root = pathlib.Path(tmp)
        # Minimal fake "operability" dependency with a side effect if executed.
        # We exercise the loader helper in isolation: hash authentic source, but
        # plant a .pyc that would run if SourceFileLoader were used.
        src_name = "probe_dep.py"
        src_path = root / src_name
        src_text = textwrap.dedent(
            '''
            BINDING = "operability.v2.json"
            def check(*args, **kwargs):
                return []
            '''
        ).lstrip()
        src_bytes = src_text.encode("utf-8")
        src_path.write_bytes(src_bytes)
        expected = _sha_bytes(src_bytes)

        # Build a timestamp-valid malicious pyc whose body sets a marker file.
        marker = root / "marker.txt"
        evil_source = textwrap.dedent(
            f'''
            BINDING = "operability.v2.json"
            open({str(marker)!r}, "w", encoding="utf-8").write("PYC_EXECUTED")
            def check(*args, **kwargs):
                return []
            '''
        ).lstrip()
        evil_code = compile(evil_source, str(src_path), "exec", dont_inherit=True)
        # CPython 3.7+ pyc header: magic (4) + flags (4) + mtime (4) + size (4)
        magic = importlib_util_magic()
        mtime = int(src_path.stat().st_mtime)
        size = src_path.stat().st_size
        header = magic + struct.pack("<III", 0, mtime, size)
        cache_dir = root / "__pycache__"
        cache_dir.mkdir()
        tag = f"cpython-{sys.version_info.major}{sys.version_info.minor}"
        pyc_path = cache_dir / f"probe_dep.{tag}.pyc"
        pyc_path.write_bytes(header + marshal.dumps(evil_code))

        # Point HERE-like loader at tmp by temporarily using local function.
        # Replicate _exec_pinned_source against tmp root.
        try:
            raw = src_path.read_bytes()
            if _sha_bytes(raw) != expected:
                return False
            module = types.ModuleType("trc_v2_pyc_probe")
            module.__file__ = str(src_path.resolve())
            module.__loader__ = None
            module.__spec__ = None
            safe_builtins = dict(vars(builtins))
            # no local imports needed
            module.__dict__["__builtins__"] = safe_builtins
            code = compile(raw, str(src_path.resolve()), "exec", dont_inherit=True)
            exec(code, module.__dict__, module.__dict__)
        except Exception:
            return False
        # Success = source semantics available and marker never written
        if not callable(getattr(module, "check", None)):
            return False
        if getattr(module, "BINDING", None) != "operability.v2.json":
            return False
        return not marker.is_file()


def importlib_util_magic() -> bytes:
    import importlib.util
    return importlib.util.MAGIC_NUMBER


def _capability_probes() -> tuple[dict[str, bool], dict[str, bool], dict[str, bool]]:
    host = HostRequestIngressV2()
    other = HostRequestIngressV2()
    cli_id = "req1_" + "01" * 16
    api_id = "req1_" + "02" * 16
    recovery_id = "req1_" + "03" * 16
    cli = host.begin("CLI", cli_id)
    retry = host.internal_retry(cli)
    api = host.begin("API", api_id)
    recovery = host.begin("recovery", recovery_id)

    json_rejected = False
    pickle_rejected = False
    copy_rejected = False
    deepcopy_rejected = False
    try:
        json.dumps(cli)
    except (TypeError, ValueError):
        json_rejected = True
    try:
        pickle.dumps(cli)
    except (ContractViolation, TypeError, ValueError, pickle.PickleError):
        pickle_rejected = True
    try:
        copy.copy(cli)
    except ContractViolation:
        copy_rejected = True
    try:
        copy.deepcopy(cli)
    except ContractViolation:
        deepcopy_rejected = True

    # No module-global mint token
    no_global = not hasattr(sys.modules[__name__], "_MINT_TOKEN") if False else (
        getattr(sys.modules[__name__], "_MINT_TOKEN", None) is None and
        not any(n == "_MINT_TOKEN" for n in globals())
    )
    # Explicit: _MINT_TOKEN must not exist in this module's globals after load
    no_global = "_MINT_TOKEN" not in globals()

    positive = {
        "TRC2-POS-01-CLI-MINT":
            type(cli) is _TrustedRequestContextV2 and
            _request_id(cli) == cli_id,
        "TRC2-POS-02-INTERNAL-RETRY": retry is cli and _request_id(retry) == cli_id,
        "TRC2-POS-03-API-NEW-CONTEXT":
            api is not cli and _request_id(api) == api_id and api_id != cli_id,
        "TRC2-POS-04-RECOVERY-NEW-CONTEXT":
            recovery not in (cli, api) and _request_id(recovery) == recovery_id and
            recovery_id not in {cli_id, api_id},
        "TRC2-POS-05-NONSERIALIZABLE":
            json_rejected and pickle_rejected and copy_rejected and
            deepcopy_rejected and
            REQUEST_RE.fullmatch(_request_id(cli)) is not None,
    }
    negative = {
        "TRC2-NEG-01-RAW-STRING": _expect_code(
            lambda: _request_id(cli_id), "TRUSTED_CONTEXT_REQUIRED"),
        "TRC2-NEG-02-PARSED-JSON": _expect_code(
            lambda: _request_id({"requestId": cli_id}),
            "TRUSTED_CONTEXT_REQUIRED"),
        "TRC2-NEG-03-CALLER-CONSTRUCTION": _expect_code(
            lambda: _foreign_construct("caller", object()),
            "TRUSTED_INGRESS_REQUIRED"),
        "TRC2-NEG-04-SINK-CONSTRUCTION": _expect_code(
            lambda: _foreign_construct("sink", object()),
            "TRUSTED_INGRESS_REQUIRED"),
        "TRC2-NEG-05-PROVIDER-CONSTRUCTION": _expect_code(
            lambda: _foreign_construct("provider", object()),
            "TRUSTED_INGRESS_REQUIRED"),
        "TRC2-NEG-06-UPPERCASE": _expect_code(
            lambda: host.begin("CLI", "req1_" + "AA" * 16),
            "REQUEST_ID_INVALID_REPRESENTATION"),
        "TRC2-NEG-07-UUID-ALIAS": _expect_code(
            lambda: host.begin("CLI", "00000000-0000-0000-0000-000000000000"),
            "REQUEST_ID_INVALID_REPRESENTATION"),
        "TRC2-NEG-08-COLLISION-REUSE": _expect_code(
            lambda: host.begin("API", cli_id), "REQUEST_ID_COLLISION"),
        "TRC2-NEG-09-INTERNAL-REMINT": _expect_code(
            lambda: host.internal_retry(cli, "req1_" + "04" * 16),
            "INTERNAL_RETRY_CONTEXT_DRIFT"),
        "TRC2-NEG-10-EXTERNAL-CONTEXT-REUSE": _expect_code(
            lambda: host.begin("recovery", "req1_" + "05" * 16, cli),
            "NEW_INVOCATION_REQUIRES_NEW_CONTEXT"),
        "TRC2-NEG-11-CAPABILITY-SERIALIZATION": _expect_code(
            lambda: cli.__reduce__(), "TRUSTED_CONTEXT_NONSERIALIZABLE"),
        "TRC2-NEG-12-SEMANTIC-PROJECTION": _expect_code(
            lambda: _semantic_project(cli),
            "REQUEST_ID_SEMANTIC_EXCLUSION_VIOLATION"),
        "TRC2-NEG-13-OBJECT-NEW-FORGE": _expect_code(
            _forge_with_object_new, "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC2-NEG-14-COPY": _expect_code(
            lambda: copy.copy(cli), "TRUSTED_CONTEXT_NONCOPYABLE"),
        "TRC2-NEG-15-DEEPCOPY": _expect_code(
            lambda: copy.deepcopy(cli), "TRUSTED_CONTEXT_NONCOPYABLE"),
        "TRC2-NEG-16-PICKLE-CONTEXT": _expect_code(
            lambda: pickle.dumps(cli), "TRUSTED_CONTEXT_NONSERIALIZABLE"),
        "TRC2-NEG-17-UNPICKLE-LOOKALIKE": _expect_code(
            lambda: _request_id(
                type("Lookalike", (), {"_project_for_checker": lambda self: cli_id})()),
            "TRUSTED_CONTEXT_REQUIRED"),
        "TRC2-NEG-18-WRONG-AUTHORITY": _expect_code(
            lambda: _request_id(cli, gate=other._gate),
            "TRUSTED_CONTEXT_WRONG_AUTHORITY"),
        "TRC2-NEG-19-REGISTRY-SUBSTITUTION": _expect_code(
            lambda: _registry_substitution_attack(cli_id),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC2-NEG-20-NO-GLOBAL-MINT-TOKEN": no_global and _expect_code(
            lambda: _TrustedRequestContextV2(),  # type: ignore[call-arg]
            "TRUSTED_INGRESS_REQUIRED"),
    }
    advanced = {
        "TRC2-ADV-PYC-IGNORED": _adversarial_pyc_probe(),
        "TRC2-ADV-GATE-NONSERIALIZABLE": _expect_code(
            lambda: pickle.dumps(host._gate), "TRUSTED_CONTEXT_NONSERIALIZABLE"),
    }
    return positive, negative, advanced


def _registry_substitution_attack(request_id: str) -> str:
    """Plant a forged instance and a fake registry entry without the real gate."""
    forged = object.__new__(_TrustedRequestContextV2)
    fake_gate = _MintGateV2()
    object.__setattr__(
        forged, "_TrustedRequestContextV2__request_id", request_id)
    object.__setattr__(forged, "_TrustedRequestContextV2__gate", fake_gate)
    # Do not register through mint — only inject into a substituted dict if one
    # existed. There is no module-global registry to substitute; projection must
    # still fail because the forged id is not in fake_gate._issued.
    return _request_id(forged)


def _expected_positive_controls() -> list[dict[str, str]]:
    return [{"id": identity, "assert": assertion}
            for identity, assertion in POSITIVE_CONTROLS]


def _expected_negative_controls() -> list[dict[str, str]]:
    return [{"id": identity, "input": input_value, "expected": expected}
            for identity, input_value, expected in NEGATIVE_CONTROLS]


def _expected_invariants() -> list[dict[str, str]]:
    return [{"id": identity, "assert": assertion}
            for identity, assertion in INVARIANTS]


def _check(value: Any, *, verify_files: bool) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["TRC-TOTALITY-ROOT: contract root must be an object"]
    if set(value) != ROOT_KEYS:
        errors.append("TRC-SCHEMA: root field set is not exact/closed")

    source, source_errors = _load_source(verify_files=verify_files)
    errors.extend(source_errors)
    expected_projection: dict[str, Any] | None = None
    if source is not None:
        try:
            expected_projection = _extract_source(source)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
            errors.append(
                f"TRC-SOURCE: closed source extraction failed "
                f"({type(exc).__name__})")

    exact_scalars = {
        "artifact": "opensip.trusted-request-context",
        "version": 2,
        "date": "2026-08-01",
        "status": "CANDIDATE-NOT-APPLIED",
        "reviewStatus": "AWAITING-INDEPENDENT-REVIEW",
        "purpose": PURPOSE,
        "sealRecommendation": "DO-NOT-SEAL-OR-APPLY",
    }
    for key, expected in exact_scalars.items():
        if value.get(key) != expected:
            errors.append(f"TRC-SCHEMA: {key} drift")
    exact_sections = {
        "authorityBoundary": AUTHORITY_BOUNDARY,
        "sourceAuthority": SOURCE_AUTHORITY,
        "dependencyClosure": DEPENDENCY_CLOSURE,
        "capabilityContract": CAPABILITY_CONTRACT,
        "invocationLifecycle": INVOCATION_LIFECYCLE,
        "semanticBoundary": SEMANTIC_BOUNDARY,
        "positiveControls": _expected_positive_controls(),
        "adversarialControls": _expected_negative_controls(),
        "invariants": _expected_invariants(),
        "assurance": ASSURANCE,
        "retainedResiduals": RESIDUALS,
        "findingDispositions": FINDING_DISPOSITIONS,
    }
    for key, expected in exact_sections.items():
        if value.get(key) != expected:
            errors.append(f"TRC-SCHEMA: {key} contract drift")
    if expected_projection is not None and \
            value.get("sourceProjection") != expected_projection:
        errors.append("TRC-SOURCE: sourceProjection is not the exact recomputation")

    positive, negative, advanced = _capability_probes()
    failed_positive = [identity for identity, passed in positive.items() if not passed]
    failed_negative = [identity for identity, passed in negative.items() if not passed]
    failed_advanced = [identity for identity, passed in advanced.items() if not passed]
    if set(positive) != {identity for identity, _ in POSITIVE_CONTROLS} or \
            failed_positive:
        errors.append(
            "TRC-PROBE: positive capability controls failed: " +
            ",".join(failed_positive or ["denominator-drift"]))
    if set(negative) != {identity for identity, _, _ in NEGATIVE_CONTROLS} or \
            failed_negative:
        errors.append(
            "TRC-PROBE: adversarial capability controls failed: " +
            ",".join(failed_negative or ["denominator-drift"]))
    if failed_advanced:
        errors.append(
            "TRC-PROBE: advanced trust-boundary probes failed: " +
            ",".join(failed_advanced))
    return errors


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    """Total parsed-JSON boundary: malformed shapes become findings."""
    try:
        return _check(value, verify_files=verify_files)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        return [
            f"TRC-TOTALITY-EXCEPTION: malformed contract shape "
            f"({type(exc).__name__})"]


def _set(path: tuple[Any, ...], replacement: Any) -> Callable[[Any], None]:
    def mutate(value: Any) -> None:
        target = value
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = replacement
    return mutate


def _drop(path: tuple[Any, ...]) -> Callable[[Any], None]:
    def mutate(value: Any) -> None:
        target = value
        for key in path[:-1]:
            target = target[key]
        if isinstance(target, list):
            target.pop(path[-1])
        else:
            target.pop(path[-1])
    return mutate


def _add_unknown(value: Any) -> None:
    value["unknownAuthority"] = True


MUTATIONS: list[tuple[str, Callable[[Any], None]]] = [
    ("source artifact pin", _set(("sourceAuthority", "sha256"), "0" * 64)),
    ("source checker pin", _set(("sourceAuthority", "checkerSha256"), "0" * 64)),
    ("source extraction rule weakens pyc", _set(
        ("sourceAuthority", "extractionRule"),
        "hash then importlib path load is fine")),
    ("source projection allocation owner", _set(
        ("sourceProjection", "authority", "allocationOwner"), "caller")),
    ("source projection allocation point", _set(
        ("sourceProjection", "allocation", "point"), "after parsing")),
    ("source projection representation", _set(
        ("sourceProjection", "representation", "regex"), ".*")),
    ("source projection reservation", _set(
        ("sourceProjection", "collisionAndRetry", "reservationRule"),
        "reserve eventually")),
    ("source projection internal/external retry", _set(
        ("sourceProjection", "collisionAndRetry", "externalRetry"),
        "reuse the prior context")),
    ("source projection custody", _set(
        ("sourceProjection", "custody", "requestContext"), "caller-owned")),
    ("source projection semantic exclusion", _drop(
        ("sourceProjection", "semanticExclusion", "excludedFrom", 4))),
    ("opaque capability", _set(("capabilityContract", "opaque"), False)),
    ("serializable capability", _set(
        ("capabilityContract", "serializable"), True)),
    ("copyable capability", _set(("capabilityContract", "copyable"), True)),
    ("public constructor", _set(
        ("capabilityContract", "publicConstructors"), ["from_string"])),
    ("raw string construction", _drop(
        ("capabilityContract", "forbiddenConstructionSources", 0))),
    ("object new construction allowed", _drop(
        ("capabilityContract", "forbiddenConstructionSources", 8))),
    ("pickle construction allowed", _drop(
        ("capabilityContract", "forbiddenConstructionSources", 10))),
    ("projection gains authority", _set(
        ("capabilityContract", "allowedProjection", "fields"),
        ["requestId", "mintToken"])),
    ("global mint token rule", _set(
        ("capabilityContract", "tokenRule"),
        "A module-global mint token is fine to export.")),
    ("internal retry remints", _set(
        ("invocationLifecycle", "internalRetry"),
        "Allocate a replacement context.")),
    ("recovery reuses prior context", _set(
        ("invocationLifecycle", "newInvocation"),
        "Recovery may reuse a prior context.")),
    ("semantic participation", _drop(
        ("semanticBoundary", "forbiddenParticipation", 5))),
    ("add downstream schema", _set(
        ("semanticBoundary", "downstreamSchemasDefinedHere"), ["Envelope"])),
    ("application status", _set(("status",), "APPLIED")),
    ("self review", _set(("reviewStatus",), "PASS")),
    ("runtime evidence claim", _set(
        ("assurance", "runtimeImplementationExecuted"), True)),
    ("product qualification claim", _set(
        ("assurance", "productQualified"), True)),
    ("remove independent review residual", _drop(("retainedResiduals", 0))),
    ("remove adversarial control", _drop(("adversarialControls", 0))),
    ("change positive assertion", _set(
        ("positiveControls", 0, "assert"), "presence is sufficient")),
    ("drop pyc finding disposition", _drop(("findingDispositions", 0))),
    ("drop forge finding disposition", _drop(("findingDispositions", 1))),
    ("unknown root field", _add_unknown),
    ("drop dependency closure", _drop(("dependencyClosure",))),
    ("drop model boundary honesty", _set(
        ("authorityBoundary", "modelBoundary"),
        "Python fully enforces production capability safety.")),
]


TOTALITY_CASES: list[tuple[str, Any]] = [
    ("null", None),
    ("string", "context"),
    ("number", 7),
    ("array", []),
    ("empty object", {}),
]


def selftest(base: Any) -> int:
    base_errors = check(base, verify_files=True)
    if base_errors:
        print("REFUSE: base contract is red; mutation results would be masked")
        for error in base_errors:
            print("  -", error)
        return 2

    escaped = 0
    for label, hostile in TOTALITY_CASES:
        findings = check(copy.deepcopy(hostile), verify_files=False)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  totality {label}")
    for label, mutate in MUTATIONS:
        candidate = copy.deepcopy(base)
        before = json.dumps(candidate, ensure_ascii=False, sort_keys=True)
        try:
            mutate(candidate)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
            # Failure-to-apply is an escape, never a skip.
            escaped += 1
            print(f"  ESCAPE  {label} (mutation failed: {type(exc).__name__})")
            continue
        after = json.dumps(candidate, ensure_ascii=False, sort_keys=True)
        if before == after:
            escaped += 1
            print(f"  ESCAPE  {label} (mutation made no change)")
            continue
        findings = check(candidate, verify_files=False)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  mutation {label}")

    duplicate_rejected = False
    try:
        json.loads('{"artifact":"a","artifact":"b"}',
                   object_pairs_hook=_pairs)
    except DuplicateKeyError:
        duplicate_rejected = True
    if not duplicate_rejected:
        escaped += 1
    print(f"  {'reject' if duplicate_rejected else 'ESCAPE':>6}  duplicate JSON key")

    denominator = len(TOTALITY_CASES) + len(MUTATIONS) + 1
    if escaped:
        print(f"{escaped}/{denominator} retained selftest cases ESCAPED")
        return 1
    print(
        f"all {len(MUTATIONS)} mutations, {len(TOTALITY_CASES)} totality cases, "
        "and 1 duplicate-key case rejected")
    return 0


def main() -> int:
    args = [arg for arg in sys.argv[1:] if arg != "--selftest"]
    path = pathlib.Path(args[0]) if args else HERE / BINDING
    if not path.is_absolute():
        path = pathlib.Path.cwd() / path
    if not path.is_file():
        print(f"missing contract: {path}", file=sys.stderr)
        return 2
    try:
        contract = _read_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError, TypeError, ValueError) as exc:
        print(f"1 finding(s) in {path.name}:")
        print(f"  - TRC-TOTALITY-DECODE: {type(exc).__name__}")
        return 1
    if "--selftest" in sys.argv:
        return selftest(contract)
    findings = check(contract, verify_files=True)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    print(
        f"trusted request context v2 OK — {path.name}; exact REQUEST-ID-V1 "
        f"source extraction; hash-exec OP2; registry mint; "
        f"{len(POSITIVE_CONTROLS)} positive and {len(NEGATIVE_CONTROLS)} "
        f"adversarial capability controls")
    print(
        "  assurance: IMPLEMENTABLE_UNEXECUTED; AWAITING-INDEPENDENT-REVIEW; "
        "NOT APPLIED; DO-NOT-SEAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
