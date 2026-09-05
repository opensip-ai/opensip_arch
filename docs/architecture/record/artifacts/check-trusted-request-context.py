#!/usr/bin/env python3
"""Design-integrity checker for TrustedRequestContextV1.

The checker hash-verifies the historical OPERABILITY authority and its
executable checker before importing any executable dependency.  It then
recomputes the closed REQUEST-ID-V1 source projection and exercises an opaque
host-only capability test double.  It does not invoke the whole OPERABILITY
checker and therefore does not inherit that checker's unrelated dependency
closure.

Usage:
  python3 -B artifacts/check-trusted-request-context.py [contract]
  python3 -B artifacts/check-trusted-request-context.py [contract] --selftest
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import pickle
import re
import sys
from typing import Any, Callable


# Keep the retained checker hygienic even if a caller omits the documented -B.
sys.dont_write_bytecode = True


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "trusted-request-context.v1.json"
SOURCE_ARTIFACT = "operability.v2.json"
SOURCE_CHECKER = "check-operability.py"
PINS = {
    SOURCE_ARTIFACT:
        "43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04",
    SOURCE_CHECKER:
        "925496916ef2c7075c02f7a767353aa6ff047cf55557304f3983e17e1c5256e2",
}
REQUEST_RE = re.compile(r"^req1_[0-9a-f]{32}$")
ROOT_KEYS = {
    "artifact", "version", "date", "status", "reviewStatus", "purpose",
    "authorityBoundary", "sourceAuthority", "sourceProjection",
    "dependencyClosure", "capabilityContract", "invocationLifecycle",
    "semanticBoundary", "positiveControls", "adversarialControls",
    "invariants", "assurance", "retainedResiduals", "sealRecommendation",
}
PURPOSE = (
    "Extract the minimum host-owned REQUEST-ID-V1 authority needed to pass an "
    "opaque TrustedRequestContextV1 across host components without making a raw "
    "RequestId, an observability envelope, or any downstream analysis contract "
    "into authority."
)
AUTHORITY_BOUNDARY = {
    "owner": "orchestration host request-ingress adapter",
    "type": "TrustedRequestContextV1",
    "rule": "Only the trusted host ingress may mint this opaque capability, and only after canonical RequestId validation and successful atomic reservation. Downstream code may project its RequestId value for closed operational correlation records but cannot construct, replace, serialize, or reinterpret the capability.",
    "nonAuthority": "This leaf does not define an event envelope, attempt identity, semantic record, storage transaction, analysis result, or product behavior.",
}
SOURCE_AUTHORITY = {
    "artifact": SOURCE_ARTIFACT,
    "sha256": PINS[SOURCE_ARTIFACT],
    "checker": SOURCE_CHECKER,
    "checkerSha256": PINS[SOURCE_CHECKER],
    "jsonPointer": "/requestIdContract",
    "sourceId": "REQUEST-ID-V1",
    "extractionRule": "The checker loads the exact pinned artifact and recomputes sourceProjection from a closed path set. The executable source checker is hash-verified before import; its whole-contract check is not invoked because this leaf intentionally does not inherit unrelated OPERABILITY dependencies.",
}
DEPENDENCY_CLOSURE = {
    "data": [SOURCE_ARTIFACT],
    "executable": [SOURCE_CHECKER],
    "rule": "No other artifact or checker is loaded. The source checker's bytes and declared binding are verified, but its whole-contract check is not executed by this leaf.",
    "forbiddenBackEdges": [
        "current OPERABILITY successor",
        "analysis evidence contract",
        "event-envelope contract",
        "attempt-identity contract",
        "delivery or projection contract",
    ],
}
CAPABILITY_CONTRACT = {
    "type": "TrustedRequestContextV1",
    "opaque": True,
    "serializable": False,
    "publicConstructors": [],
    "mintOwner": "HostRequestIngressV1",
    "mintPreconditions": [
        "the candidate decodes as exactly sixteen bytes under REQUEST-ID-V1",
        "the candidate is atomically reserved under the host RequestId registry's unique constraint",
        "the invocation has crossed trusted ingress and has not yet published a child operation",
    ],
    "forbiddenConstructionSources": [
        "raw string", "parsed JSON", "public caller", "event sink",
        "provider", "stage", "profile", "projection adapter",
    ],
    "allowedProjection": {
        "method": "request_id(TrustedRequestContextV1) -> RequestIdV1",
        "fields": ["requestId"],
        "representation": "^req1_[0-9a-f]{32}$",
        "persistence": "The projected value may enter only a downstream closed operational-correlation record. The capability and its mint authority never serialize.",
    },
    "tokenRule": "Any private constructor token or host registry handle is process-local, nonserializable, absent from the RequestId projection, and never accepted as caller data.",
}
INVOCATION_LIFECYCLE = {
    "acceptedKinds": ["CLI", "API", "recovery"],
    "internalRetry": "An internal retry inside one accepted invocation receives the identical TrustedRequestContextV1 capability and identical RequestId; it performs no new allocation or reservation.",
    "newInvocation": "Every new CLI, API, or recovery invocation allocates and reserves a new canonical RequestId and receives a distinct TrustedRequestContextV1. A prior capability cannot be supplied as the new invocation's authority.",
    "transportRetry": "A transport retry that crosses trusted ingress is a new invocation. A retry wholly contained inside the accepted host invocation is internalRetry.",
    "collision": "A reserved RequestId cannot mint a second context. Collision handling remains owned by the pinned REQUEST-ID-V1 source and never overwrites or aliases the existing reservation.",
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
    "rule": "Neither the capability nor its projected RequestId is an analysis input or evidence authority. Only explicitly downstream operational schemas may persist the projection.",
    "forbiddenParticipation": SEMANTIC_EXCLUSIONS,
    "downstreamSchemasDefinedHere": [],
}
POSITIVE_CONTROLS = [
    ("TRC-POS-01-CLI-MINT",
     "A canonical unreserved candidate at trusted CLI ingress yields one opaque context and the exact RequestId projection."),
    ("TRC-POS-02-INTERNAL-RETRY",
     "Internal retry returns the identical capability without allocation or reservation."),
    ("TRC-POS-03-API-NEW-CONTEXT",
     "A new API invocation receives a distinct context with a distinct reserved RequestId."),
    ("TRC-POS-04-RECOVERY-NEW-CONTEXT",
     "A new recovery invocation receives a distinct context with a distinct reserved RequestId."),
    ("TRC-POS-05-NONSERIALIZABLE",
     "JSON and object serialization reject the capability while its RequestId projection remains canonical text."),
]
NEGATIVE_CONTROLS = [
    ("TRC-NEG-01-RAW-STRING", "raw string as context", "TRUSTED_CONTEXT_REQUIRED"),
    ("TRC-NEG-02-PARSED-JSON", "parsed JSON object as context", "TRUSTED_CONTEXT_REQUIRED"),
    ("TRC-NEG-03-CALLER-CONSTRUCTION", "public caller constructs context", "TRUSTED_INGRESS_REQUIRED"),
    ("TRC-NEG-04-SINK-CONSTRUCTION", "event sink constructs context", "TRUSTED_INGRESS_REQUIRED"),
    ("TRC-NEG-05-PROVIDER-CONSTRUCTION", "provider constructs context", "TRUSTED_INGRESS_REQUIRED"),
    ("TRC-NEG-06-UPPERCASE", "uppercase RequestId", "REQUEST_ID_INVALID_REPRESENTATION"),
    ("TRC-NEG-07-UUID-ALIAS", "UUID-shaped alias", "REQUEST_ID_INVALID_REPRESENTATION"),
    ("TRC-NEG-08-COLLISION-REUSE", "already reserved RequestId", "REQUEST_ID_COLLISION"),
    ("TRC-NEG-09-INTERNAL-REMINT", "internal retry remints context", "INTERNAL_RETRY_CONTEXT_DRIFT"),
    ("TRC-NEG-10-EXTERNAL-CONTEXT-REUSE", "new invocation supplies prior context", "NEW_INVOCATION_REQUIRES_NEW_CONTEXT"),
    ("TRC-NEG-11-CAPABILITY-SERIALIZATION", "serialize opaque capability", "TRUSTED_CONTEXT_NONSERIALIZABLE"),
    ("TRC-NEG-12-SEMANTIC-PROJECTION", "project context into semantic input", "REQUEST_ID_SEMANTIC_EXCLUSION_VIOLATION"),
]
INVARIANTS = [
    ("TRC-1", "The source projection is recomputed from the exact pinned REQUEST-ID-V1 authority rather than trusted as authored presence."),
    ("TRC-2", "Only host ingress can mint TrustedRequestContextV1 and only after canonical validation plus successful reservation."),
    ("TRC-3", "Raw strings, parsed JSON, callers, sinks, providers, stages, profiles, and adapters cannot substitute for the opaque capability."),
    ("TRC-4", "The capability exposes exactly one canonical RequestId projection and is itself nonserializable."),
    ("TRC-5", "Internal retry retains one context; every new CLI, API, or recovery invocation gets a distinct newly reserved context."),
    ("TRC-6", "RequestId remains operational-only and cannot influence any enumerated semantic identity or result."),
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
        "effect": "No consumer may treat this candidate as accepted authority until a reviewer independently reconstructs the source extraction and capability probes.",
    },
    {
        "id": "PRODUCTION-CAPABILITY-IMPLEMENTATION",
        "state": "UNEXECUTED",
        "effect": "The checker uses an in-process opaque test double; no Rust visibility boundary, allocator, registry, restart, or concurrency implementation has been demonstrated.",
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


def _sha_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _import_verified_source_checker() -> Any:
    """Import only after the caller has verified every executable pin."""
    spec = importlib.util.spec_from_file_location(
        "trusted_request_context_pinned_operability", HERE / SOURCE_CHECKER)
    if spec is None or spec.loader is None:
        raise ImportError(SOURCE_CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_source(*, verify_files: bool) -> tuple[Any | None, list[str]]:
    errors: list[str] = []
    if verify_files:
        observed: dict[str, str] = {}
        for filename, expected in PINS.items():
            path = HERE / filename
            if not path.is_file():
                errors.append(f"TRC-SOURCE: missing pinned input {filename}")
                continue
            observed[filename] = _sha_file(path)
            if observed[filename] != expected:
                errors.append(
                    f"TRC-SOURCE: pin drift {filename}: "
                    f"{observed[filename]} != {expected}")
        # No executable dependency is imported when any pin is wrong.
        if errors:
            return None, errors
        try:
            source_checker = _import_verified_source_checker()
            if source_checker.BINDING != SOURCE_ARTIFACT or \
                    not callable(source_checker.check):
                errors.append("TRC-SOURCE: pinned checker API/binding drift")
        except Exception as exc:
            errors.append(
                f"TRC-SOURCE: pinned checker import failed "
                f"({type(exc).__name__})")
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


_MINT_TOKEN = object()


class _TrustedRequestContextV1:
    __slots__ = ("__request_id",)

    def __init__(self, token: object, request_id: str) -> None:
        if token is not _MINT_TOKEN:
            raise ContractViolation("TRUSTED_INGRESS_REQUIRED")
        if not isinstance(request_id, str) or not REQUEST_RE.fullmatch(request_id):
            raise ContractViolation("REQUEST_ID_INVALID_REPRESENTATION")
        self.__request_id = request_id

    def _project_for_checker(self) -> str:
        return self.__request_id

    def __reduce__(self) -> Any:
        raise ContractViolation("TRUSTED_CONTEXT_NONSERIALIZABLE")

    def __reduce_ex__(self, protocol: int) -> Any:
        del protocol
        raise ContractViolation("TRUSTED_CONTEXT_NONSERIALIZABLE")


class _HostRequestIngressV1:
    __slots__ = ("_reservations",)

    def __init__(self) -> None:
        self._reservations: set[str] = set()

    def begin(self, kind: Any, candidate: Any,
              prior_context: Any = None) -> _TrustedRequestContextV1:
        if kind not in {"CLI", "API", "recovery"}:
            raise ContractViolation("TRUSTED_INGRESS_REQUIRED")
        if prior_context is not None:
            raise ContractViolation("NEW_INVOCATION_REQUIRES_NEW_CONTEXT")
        if not isinstance(candidate, str) or not REQUEST_RE.fullmatch(candidate):
            raise ContractViolation("REQUEST_ID_INVALID_REPRESENTATION")
        if candidate in self._reservations:
            raise ContractViolation("REQUEST_ID_COLLISION")
        self._reservations.add(candidate)
        return _TrustedRequestContextV1(_MINT_TOKEN, candidate)

    def internal_retry(
            self, context: Any, replacement_candidate: Any = None
    ) -> _TrustedRequestContextV1:
        if not isinstance(context, _TrustedRequestContextV1):
            raise ContractViolation("TRUSTED_CONTEXT_REQUIRED")
        if replacement_candidate is not None:
            raise ContractViolation("INTERNAL_RETRY_CONTEXT_DRIFT")
        return context


def _request_id(context: Any) -> str:
    if not isinstance(context, _TrustedRequestContextV1):
        raise ContractViolation("TRUSTED_CONTEXT_REQUIRED")
    value = context._project_for_checker()
    if not REQUEST_RE.fullmatch(value):
        raise ContractViolation("REQUEST_ID_INVALID_REPRESENTATION")
    return value


def _foreign_construct(origin: str, value: Any) -> _TrustedRequestContextV1:
    del origin
    return _TrustedRequestContextV1(value, "req1_" + "0" * 32)


def _semantic_project(context: Any) -> None:
    if isinstance(context, _TrustedRequestContextV1):
        raise ContractViolation("REQUEST_ID_SEMANTIC_EXCLUSION_VIOLATION")
    raise ContractViolation("TRUSTED_CONTEXT_REQUIRED")


def _expect_code(action: Callable[[], Any], code: str) -> bool:
    try:
        action()
    except ContractViolation as exc:
        return exc.code == code
    except (AttributeError, IndexError, KeyError, TypeError, ValueError):
        return False
    return False


def _capability_probes() -> tuple[dict[str, bool], dict[str, bool]]:
    host = _HostRequestIngressV1()
    cli_id = "req1_" + "01" * 16
    api_id = "req1_" + "02" * 16
    recovery_id = "req1_" + "03" * 16
    cli = host.begin("CLI", cli_id)
    retry = host.internal_retry(cli)
    api = host.begin("API", api_id)
    recovery = host.begin("recovery", recovery_id)

    json_rejected = False
    pickle_rejected = False
    try:
        json.dumps(cli)
    except (TypeError, ValueError):
        json_rejected = True
    try:
        pickle.dumps(cli)
    except (ContractViolation, TypeError, ValueError, pickle.PickleError):
        pickle_rejected = True

    positive = {
        "TRC-POS-01-CLI-MINT":
            isinstance(cli, _TrustedRequestContextV1) and
            _request_id(cli) == cli_id,
        "TRC-POS-02-INTERNAL-RETRY": retry is cli and _request_id(retry) == cli_id,
        "TRC-POS-03-API-NEW-CONTEXT":
            api is not cli and _request_id(api) == api_id and api_id != cli_id,
        "TRC-POS-04-RECOVERY-NEW-CONTEXT":
            recovery not in (cli, api) and _request_id(recovery) == recovery_id and
            recovery_id not in {cli_id, api_id},
        "TRC-POS-05-NONSERIALIZABLE":
            json_rejected and pickle_rejected and
            REQUEST_RE.fullmatch(_request_id(cli)) is not None,
    }
    negative = {
        "TRC-NEG-01-RAW-STRING": _expect_code(
            lambda: _request_id(cli_id), "TRUSTED_CONTEXT_REQUIRED"),
        "TRC-NEG-02-PARSED-JSON": _expect_code(
            lambda: _request_id({"requestId": cli_id}),
            "TRUSTED_CONTEXT_REQUIRED"),
        "TRC-NEG-03-CALLER-CONSTRUCTION": _expect_code(
            lambda: _foreign_construct("caller", object()),
            "TRUSTED_INGRESS_REQUIRED"),
        "TRC-NEG-04-SINK-CONSTRUCTION": _expect_code(
            lambda: _foreign_construct("sink", object()),
            "TRUSTED_INGRESS_REQUIRED"),
        "TRC-NEG-05-PROVIDER-CONSTRUCTION": _expect_code(
            lambda: _foreign_construct("provider", object()),
            "TRUSTED_INGRESS_REQUIRED"),
        "TRC-NEG-06-UPPERCASE": _expect_code(
            lambda: host.begin("CLI", "req1_" + "AA" * 16),
            "REQUEST_ID_INVALID_REPRESENTATION"),
        "TRC-NEG-07-UUID-ALIAS": _expect_code(
            lambda: host.begin("CLI", "00000000-0000-0000-0000-000000000000"),
            "REQUEST_ID_INVALID_REPRESENTATION"),
        "TRC-NEG-08-COLLISION-REUSE": _expect_code(
            lambda: host.begin("API", cli_id), "REQUEST_ID_COLLISION"),
        "TRC-NEG-09-INTERNAL-REMINT": _expect_code(
            lambda: host.internal_retry(cli, "req1_" + "04" * 16),
            "INTERNAL_RETRY_CONTEXT_DRIFT"),
        "TRC-NEG-10-EXTERNAL-CONTEXT-REUSE": _expect_code(
            lambda: host.begin("recovery", "req1_" + "05" * 16, cli),
            "NEW_INVOCATION_REQUIRES_NEW_CONTEXT"),
        "TRC-NEG-11-CAPABILITY-SERIALIZATION": _expect_code(
            lambda: cli.__reduce__(), "TRUSTED_CONTEXT_NONSERIALIZABLE"),
        "TRC-NEG-12-SEMANTIC-PROJECTION": _expect_code(
            lambda: _semantic_project(cli),
            "REQUEST_ID_SEMANTIC_EXCLUSION_VIOLATION"),
    }
    return positive, negative


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
        "version": 1,
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
    }
    for key, expected in exact_sections.items():
        if value.get(key) != expected:
            errors.append(f"TRC-SCHEMA: {key} contract drift")
    if expected_projection is not None and \
            value.get("sourceProjection") != expected_projection:
        errors.append("TRC-SOURCE: sourceProjection is not the exact recomputation")

    positive, negative = _capability_probes()
    failed_positive = [identity for identity, passed in positive.items() if not passed]
    failed_negative = [identity for identity, passed in negative.items() if not passed]
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
    ("public constructor", _set(
        ("capabilityContract", "publicConstructors"), ["from_string"])),
    ("raw string construction", _drop(
        ("capabilityContract", "forbiddenConstructionSources", 0))),
    ("caller construction", _drop(
        ("capabilityContract", "forbiddenConstructionSources", 2))),
    ("sink construction", _drop(
        ("capabilityContract", "forbiddenConstructionSources", 3))),
    ("provider construction", _drop(
        ("capabilityContract", "forbiddenConstructionSources", 4))),
    ("projection gains authority", _set(
        ("capabilityContract", "allowedProjection", "fields"),
        ["requestId", "mintToken"])),
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
    ("unknown root field", _add_unknown),
    ("drop dependency closure", _drop(("dependencyClosure",))),
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
        f"trusted request context OK — {path.name}; exact REQUEST-ID-V1 "
        f"source extraction; {len(POSITIVE_CONTROLS)} positive and "
        f"{len(NEGATIVE_CONTROLS)} adversarial capability controls")
    print("  assurance: IMPLEMENTABLE_UNEXECUTED; AWAITING-INDEPENDENT-REVIEW; NOT APPLIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
