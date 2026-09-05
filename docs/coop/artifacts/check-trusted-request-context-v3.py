#!/usr/bin/env python3
"""Design-integrity checker for the TrustedRequestContext v3 successor.

V3 responds to the exact independent rejection of v2.  The context is a
fieldless identity object.  One selected TrustedHostRequestAuthorityV3 owns an
out-of-band ledger state containing both the exactly-once RequestId reservation
and the exact context object.  Projection is a method of that authority and
never consumes authority supplied by the context or caller.

This is a trusted-host API/provenance model, not a Python sandbox.  Arbitrary
same-process private-state inspection/mutation, memory writes, and debugger
compromise are explicitly outside its claim.  Production Rust capability
ownership and durable atomic reservation remain UNEXECUTED gates.

Usage:
  python3 -B artifacts/check-trusted-request-context-v3.py [contract]
  python3 -B artifacts/check-trusted-request-context-v3.py [contract] --selftest
"""
from __future__ import annotations

import ast
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

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
BINDING = "trusted-request-context.v3.json"
SOURCE_ARTIFACT = "operability.v2.json"
SOURCE_CHECKER = "check-operability.py"
PREDECESSOR = "trusted-request-context.v2.json"
REJECTION = "trusted-request-context.v2.review-independent-prefreeze.json"

PINS = {
    "trusted-request-context.v1.json":
        "57183e437d4242df052db5d3c111389fd2865fc9bc02b1e9667322bdfeaedf03",
    "check-trusted-request-context.py":
        "70548f967d7b78e424da3697f2222ac96ae271978a7532ae90ebca9dd9e55490",
    "trusted-request-context.v1.review-independent-prefreeze.json":
        "5072ea0d9d5879522987c69d5a53c332d0520c6e01804347c47b1935efb3f9f7",
    PREDECESSOR:
        "df38a7e3a77169655baca38e9c494a9e4197bdab6737bec77085c3d49b0dc917",
    "check-trusted-request-context-v2.py":
        "4419ead424c13a8b5b6b82bc6fa1192d123a90795613fe836b85fdbaf634a3dd",
    "trusted-request-context.v2.adjudication-v1-rejection-response.json":
        "bff86b9bcf9f10519256a219feb1a47b0ca2d3dfde8b41913716113fa54235ba",
    REJECTION:
        "fbb82c379ccc238c9a635395601f8d2fd9ff094fbe84bd0ee9c47b265b51d7aa",
    SOURCE_ARTIFACT:
        "43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04",
    SOURCE_CHECKER:
        "925496916ef2c7075c02f7a767353aa6ff047cf55557304f3983e17e1c5256e2",
}

DECLARED_EXECUTABLE = frozenset({SOURCE_CHECKER})
REQUEST_RE = re.compile(r"^req1_[0-9a-f]{32}$")

CHANGED_ROOT_KEYS = {
    "version", "purpose", "authorityBoundary", "dependencyClosure",
    "capabilityContract", "invocationLifecycle", "positiveControls",
    "adversarialControls", "invariants", "retainedResiduals",
    "findingDispositions",
}
ADDED_ROOT_KEYS = {"successorDelta"}
PROTECTED_ROOT_KEYS = (
    "artifact", "date", "status", "reviewStatus", "sourceAuthority",
    "sourceProjection", "semanticBoundary", "assurance",
    "sealRecommendation",
)
SUCCESSOR_DELTA = {
    "predecessor": (
        "trusted-request-context.v2.json@"
        "df38a7e3a77169655baca38e9c494a9e4197bdab6737bec77085c3d49b0dc917"
    ),
    "predecessorChecker": (
        "check-trusted-request-context-v2.py@"
        "4419ead424c13a8b5b6b82bc6fa1192d123a90795613fe836b85fdbaf634a3dd"
    ),
    "predecessorAdjudication": (
        "trusted-request-context.v2.adjudication-v1-rejection-response.json@"
        "bff86b9bcf9f10519256a219feb1a47b0ca2d3dfde8b41913716113fa54235ba"
    ),
    "rejection": (
        "trusted-request-context.v2.review-independent-prefreeze.json@"
        "fbb82c379ccc238c9a635395601f8d2fd9ff094fbe84bd0ee9c47b265b51d7aa"
    ),
    "changedRootKeys": [
        "version", "purpose", "authorityBoundary", "dependencyClosure",
        "capabilityContract", "invocationLifecycle", "positiveControls",
        "adversarialControls", "invariants", "retainedResiduals",
        "findingDispositions",
    ],
    "addedRootKeys": ["successorDelta"],
    "protectedRootKeys": list(PROTECTED_ROOT_KEYS),
    "scope": (
        "The v3 checker loads the exact pinned v2 predecessor, compares every "
        "unlisted predecessor root value for exact equality, rejects additions "
        "outside addedRootKeys, and recomputes the changed authority claims "
        "with executable probes. No text-substring or authored boolean is a "
        "successor oracle."
    ),
}

# Closed declarations are bound independently of the candidate.  Executable
# probes below recompute their behavioral claims; these digests bind the exact
# narrative/control values and make every nested object closed.
CHANGED_SECTION_SHA256 = {
    "purpose": "3dcdc151e1a491b57d4c3804872636fb8b9394ebc5b56fdfac5576495434ba35",
    "authorityBoundary": "7289b3dd7e81bcf6bb2bd0be7063145ff3ce316e03cd26f79a8f98f9a45f4b38",
    "dependencyClosure": "7f01a033d09912486f0f10b21b3102a3cbca4f54111920169d4f4610d0331b82",
    "capabilityContract": "6d38d4563360a34cae68e396c43ad543c1ee8c7df207de18534624409829332a",
    "invocationLifecycle": "96b78ceaa5e33a6c307e94ce7145cc4754dd1bce3cc1022c140454c8dc832a91",
    "positiveControls": "0718b21c1305461ff4555703a7994769c97e23feacae2fbe190059146278978f",
    "adversarialControls": "f518356a3a342beadd14436a94eb781185cf0cced61a31d61629f137d03c78a6",
    "invariants": "4b86a8ead7720667de5292759e08ef007c8985936a327ab129c5ebf59ee903a0",
    "retainedResiduals": "3a05d77ddd6eb3e1519921a6a2a66024fcc3e24a9870d332cf7c48573fe5807d",
    "findingDispositions": "2bf0a79ce1db7e2f6d0ea948fbd1e93d0c23f81530c357861e542de313d66213",
}

POSITIVE_IDS = (
    "TRC3-POS-01-CLI-EXACT-BINDING",
    "TRC3-POS-02-INTERNAL-RETRY",
    "TRC3-POS-03-API-NEW-CONTEXT",
    "TRC3-POS-04-RECOVERY-NEW-CONTEXT",
    "TRC3-POS-05-NONSERIALIZABLE",
)
NEGATIVE_CODES = (
    ("TRC3-NEG-01-RAW-STRING", "TRUSTED_CONTEXT_REQUIRED"),
    ("TRC3-NEG-02-PARSED-JSON", "TRUSTED_CONTEXT_REQUIRED"),
    ("TRC3-NEG-03-CALLER-CONSTRUCTION", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC3-NEG-04-SINK-CONSTRUCTION", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC3-NEG-05-PROVIDER-CONSTRUCTION", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC3-NEG-06-STAGE-CONSTRUCTION", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC3-NEG-07-PROFILE-CONSTRUCTION", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC3-NEG-08-PROJECTION-ADAPTER-CONSTRUCTION", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC3-NEG-09-UPPERCASE", "REQUEST_ID_INVALID_REPRESENTATION"),
    ("TRC3-NEG-10-UUID-ALIAS", "REQUEST_ID_INVALID_REPRESENTATION"),
    ("TRC3-NEG-11-COLLISION-REUSE", "REQUEST_ID_COLLISION"),
    ("TRC3-NEG-12-INTERNAL-REMINT", "INTERNAL_RETRY_CONTEXT_DRIFT"),
    ("TRC3-NEG-13-EXTERNAL-CONTEXT-REUSE", "NEW_INVOCATION_REQUIRES_NEW_CONTEXT"),
    ("TRC3-NEG-14-CAPABILITY-SERIALIZATION", "TRUSTED_CONTEXT_NONSERIALIZABLE"),
    ("TRC3-NEG-15-SEMANTIC-PROJECTION", "REQUEST_ID_SEMANTIC_EXCLUSION_VIOLATION"),
    ("TRC3-NEG-16-OBJECT-NEW-FORGE", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC3-NEG-17-COPY", "TRUSTED_CONTEXT_NONCOPYABLE"),
    ("TRC3-NEG-18-DEEPCOPY", "TRUSTED_CONTEXT_NONCOPYABLE"),
    ("TRC3-NEG-19-PICKLE-CONTEXT", "TRUSTED_CONTEXT_NONSERIALIZABLE"),
    ("TRC3-NEG-20-UNPICKLE-LOOKALIKE", "TRUSTED_CONTEXT_REQUIRED"),
    ("TRC3-NEG-21-INDEPENDENT-AUTHORITY", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC3-NEG-22-POPULATED-REGISTRY-SUBSTITUTION", "TRUSTED_AUTHORITY_PARAMETER_FORBIDDEN"),
    ("TRC3-NEG-23-NEW-GATE-AND-MINT-EQUIVALENT", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC3-NEG-24-NO-GLOBAL-SHARED-MINT-AUTHORITY", "NO_SHARED_MINT_AUTHORITY"),
    ("TRC3-NEG-25-DIRECT-NO-INGRESS-ALLOCATION", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC3-NEG-26-CONTEXT-AUTHORITY-LEAK", "TRUSTED_CONTEXT_AUTHORITY_OPAQUE"),
    ("TRC3-NEG-27-DUPLICATE-CONTEXT", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC3-NEG-28-UNRESERVED-CONTEXT", "TRUSTED_CONTEXT_UNREGISTERED"),
    ("TRC3-NEG-29-CALLER-REGISTRY-ARGUMENT", "TRUSTED_AUTHORITY_PARAMETER_FORBIDDEN"),
    ("TRC3-NEG-30-CONTEXT-SLOT-INJECTION", "TRUSTED_CONTEXT_AUTHORITY_OPAQUE"),
)


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


def _canonical_digest(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return _sha_bytes(raw)


def _exec_pinned_source(
        filename: str,
        expected_sha: str,
        *,
        allow_local: frozenset[str],
        root: pathlib.Path | None = None,
) -> types.ModuleType:
    """Hash, compile, and execute one source buffer; never select a .pyc."""
    source_root = HERE if root is None else root.resolve()
    path = source_root / filename
    if not path.is_file():
        raise FileNotFoundError(filename)
    raw = path.read_bytes()
    observed = _sha_bytes(raw)
    if observed != expected_sha:
        raise ValueError(f"pin drift {filename}: {observed} != {expected_sha}")

    module_name = f"trc_v3_pinned_{filename.replace('.', '_').replace('-', '_')}"
    module = types.ModuleType(module_name)
    module.__file__ = str(path.resolve())
    module.__package__ = None
    module.__loader__ = None
    module.__spec__ = None

    real_import = builtins.__import__

    def _is_under_root(file_name: str | None) -> bool:
        if file_name is None:
            return False
        try:
            pathlib.Path(file_name).resolve().relative_to(source_root)
            return True
        except (OSError, ValueError):
            return False

    def guarded_import(
            name: str,
            globals_value: Any = None,
            locals_value: Any = None,
            fromlist: Any = (),
            level: int = 0,
    ) -> Any:
        del globals_value, locals_value, fromlist
        if level != 0 or name.startswith("."):
            raise ImportError(f"TRC-SOURCE: relative import forbidden: {name}")
        top = name.split(".", 1)[0]
        local_candidate = source_root / f"{top}.py"
        if local_candidate.is_file():
            if local_candidate.name not in allow_local:
                raise ImportError(
                    f"TRC-SOURCE: undeclared local import rejected: {name}")
            raise ImportError(
                f"TRC-SOURCE: nested local import must be pre-authenticated: "
                f"{name}")
        if name in sys.modules:
            existing = sys.modules[name]
            if _is_under_root(getattr(existing, "__file__", None)):
                raise ImportError(f"TRC-SOURCE: refuse cached local module: {name}")
            return existing
        imported = real_import(name)
        if _is_under_root(getattr(imported, "__file__", None)):
            raise ImportError(
                f"TRC-SOURCE: refuse local path import via stdlib loader: {name}")
        return imported

    safe_builtins = dict(vars(builtins))
    safe_builtins["__import__"] = guarded_import
    module.__dict__["__builtins__"] = safe_builtins
    code = compile(raw, str(path.resolve()), "exec", dont_inherit=True)
    exec(code, module.__dict__, module.__dict__)
    return module


def _verify_pins() -> list[str]:
    errors: list[str] = []
    for filename, expected in PINS.items():
        path = HERE / filename
        if not path.is_file():
            errors.append(f"TRC3-PIN: missing frozen input {filename}")
            continue
        observed = _sha_file(path)
        if observed != expected:
            errors.append(
                f"TRC3-PIN: drift {filename}: {observed} != {expected}")
    return errors


def _load_source(*, verify_files: bool) -> tuple[Any | None, list[str]]:
    errors = _verify_pins() if verify_files else []
    if errors:
        return None, errors
    if verify_files:
        try:
            source_checker = _exec_pinned_source(
                SOURCE_CHECKER,
                PINS[SOURCE_CHECKER],
                allow_local=DECLARED_EXECUTABLE,
            )
            if getattr(source_checker, "BINDING", None) != SOURCE_ARTIFACT or \
                    not callable(getattr(source_checker, "check", None)):
                errors.append("TRC3-SOURCE: pinned checker API/binding drift")
        except Exception as exc:
            errors.append(
                "TRC3-SOURCE: pinned checker secure-exec failed "
                f"({type(exc).__name__}: {exc})")
    if errors:
        return None, errors
    try:
        return _read_json(HERE / SOURCE_ARTIFACT), []
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError,
            TypeError, ValueError) as exc:
        return None, [
            "TRC3-SOURCE: source artifact could not be decoded "
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


class _TrustedRequestContextV3:
    """Fieldless identity object.  It contains no authenticity material."""

    __slots__ = ()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        del args, kwargs
        raise ContractViolation("TRUSTED_INGRESS_REQUIRED")

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


class TrustedHostRequestAuthorityV3:
    """One independently rooted host authority and its out-of-band registry."""

    __slots__ = ("__state",)

    def __init__(self) -> None:
        # RequestId -> (reservation count, exact context object).  One immutable
        # state reference models reservation and registration as one ledger
        # transition; durable atomicity remains explicitly UNEXECUTED.
        self.__state: dict[str, tuple[int, _TrustedRequestContextV3]] = {}

    def begin(
            self,
            kind: Any,
            candidate: Any,
            prior_context: Any = None,
    ) -> _TrustedRequestContextV3:
        if kind not in {"CLI", "API", "recovery"}:
            raise ContractViolation("TRUSTED_INGRESS_REQUIRED")
        if prior_context is not None:
            raise ContractViolation("NEW_INVOCATION_REQUIRES_NEW_CONTEXT")
        if not isinstance(candidate, str) or not REQUEST_RE.fullmatch(candidate):
            raise ContractViolation("REQUEST_ID_INVALID_REPRESENTATION")
        state = self.__state
        if candidate in state:
            raise ContractViolation("REQUEST_ID_COLLISION")

        # The only allocation that can enter this authority's state is inside
        # this trusted operation.  Build the whole next state before one commit.
        context = object.__new__(_TrustedRequestContextV3)
        next_state = dict(state)
        next_state[candidate] = (1, context)
        self.__state = next_state
        return context

    def internal_retry(
            self,
            context: Any,
            replacement_candidate: Any = None,
    ) -> _TrustedRequestContextV3:
        self.request_id(context)
        if replacement_candidate is not None:
            raise ContractViolation("INTERNAL_RETRY_CONTEXT_DRIFT")
        return context

    def request_id(
            self,
            context: Any,
            *authority_args: Any,
            **authority_kwargs: Any,
    ) -> str:
        # The API is defensive at its dynamic boundary: a caller cannot supply
        # a substitute registry/authority even as an extra Python argument.
        if authority_args or authority_kwargs:
            raise ContractViolation("TRUSTED_AUTHORITY_PARAMETER_FORBIDDEN")
        if type(context) is not _TrustedRequestContextV3:
            raise ContractViolation("TRUSTED_CONTEXT_REQUIRED")
        state = self.__state
        if not isinstance(state, dict):
            raise ContractViolation("TRUSTED_AUTHORITY_REGISTRY_CORRUPT")
        matches: list[tuple[str, int]] = []
        for request_id, binding in state.items():
            if not isinstance(binding, tuple) or len(binding) != 2:
                raise ContractViolation("TRUSTED_AUTHORITY_REGISTRY_CORRUPT")
            count, bound_context = binding
            if bound_context is context:
                matches.append((request_id, count))
        if not matches:
            raise ContractViolation("TRUSTED_CONTEXT_UNREGISTERED")
        if len(matches) != 1:
            raise ContractViolation("TRUSTED_AUTHORITY_REGISTRY_CORRUPT")
        request_id, count = matches[0]
        if count != 1 or not isinstance(request_id, str) or \
                REQUEST_RE.fullmatch(request_id) is None:
            raise ContractViolation("TRUSTED_AUTHORITY_REGISTRY_CORRUPT")
        return request_id


def _authority_state_fingerprint(
        authority: TrustedHostRequestAuthorityV3,
) -> tuple[tuple[str, int, int], ...]:
    """Checker-only observation; never an authority or product API."""
    state = object.__getattribute__(
        authority, "_TrustedHostRequestAuthorityV3__state")
    if not isinstance(state, dict):
        return (("<corrupt>", -1, -1),)
    rows: list[tuple[str, int, int]] = []
    for request_id, binding in state.items():
        if not isinstance(binding, tuple) or len(binding) != 2:
            return (("<corrupt>", -1, -1),)
        count, context = binding
        rows.append((request_id, count, id(context)))
    return tuple(sorted(rows))


def _reservation_count(
        authority: TrustedHostRequestAuthorityV3, request_id: str
) -> int | None:
    state = object.__getattribute__(
        authority, "_TrustedHostRequestAuthorityV3__state")
    binding = state.get(request_id) if isinstance(state, dict) else None
    if isinstance(binding, tuple) and len(binding) == 2:
        return binding[0]
    return None


# Six genuinely distinct untrusted construction routes.  They share no helper
# and none can write a selected authority's out-of-band state.
def _caller_construction_route() -> _TrustedRequestContextV3:
    return object.__new__(_TrustedRequestContextV3)


def _sink_construction_route() -> _TrustedRequestContextV3:
    candidate = object.__new__(_TrustedRequestContextV3)
    return candidate


def _provider_construction_route() -> _TrustedRequestContextV3:
    provider_value = object.__new__(_TrustedRequestContextV3)
    return provider_value


def _stage_construction_route() -> _TrustedRequestContextV3:
    stage_output = object.__new__(_TrustedRequestContextV3)
    return stage_output


def _profile_construction_route() -> _TrustedRequestContextV3:
    profile_context = object.__new__(_TrustedRequestContextV3)
    return profile_context


def _projection_adapter_construction_route() -> _TrustedRequestContextV3:
    adapter_context = object.__new__(_TrustedRequestContextV3)
    return adapter_context


def _semantic_project(context: Any) -> None:
    if type(context) is _TrustedRequestContextV3:
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


def _retained_negative(
        authority: TrustedHostRequestAuthorityV3,
        action: Callable[[], Any],
        code: str,
) -> bool:
    before = _authority_state_fingerprint(authority)
    rejected = _expect_code(action, code)
    after = _authority_state_fingerprint(authority)
    return rejected and before == after


def _populated_registry_substitution(
        authority: TrustedHostRequestAuthorityV3, request_id: str
) -> str:
    forged = object.__new__(_TrustedRequestContextV3)
    substitute_registry = {request_id: (1, forged)}
    if substitute_registry[request_id] != (1, forged):
        raise AssertionError("substitute registry was not populated")
    return authority.request_id(
        forged, caller_registry=substitute_registry)


def _duplicate_context_attack(
        authority: TrustedHostRequestAuthorityV3, reserved_id: str
) -> str:
    duplicate = object.__new__(_TrustedRequestContextV3)
    attacker_binding = {reserved_id: (1, duplicate)}
    if attacker_binding[reserved_id][1] is not duplicate:
        raise AssertionError("duplicate attack was not constructed")
    # The attacker's claimed binding is deliberately not an authority input.
    return authority.request_id(duplicate)


def _unreserved_context_attack(
        authority: TrustedHostRequestAuthorityV3, unreserved_id: str
) -> str:
    forged = object.__new__(_TrustedRequestContextV3)
    attacker_binding = {unreserved_id: (1, forged)}
    if attacker_binding[unreserved_id][1] is not forged:
        raise AssertionError("unreserved attack was not constructed")
    return authority.request_id(forged)


def _attempt_context_authority_leak(context: _TrustedRequestContextV3) -> Any:
    leaked_names = (
        "requestId", "request_id", "_request_id", "authority", "_authority",
        "gate", "_gate", "_gate_for_checker", "registry", "_registry",
        "token", "_token", "mint", "_mint", "project", "_project_for_checker",
        "__dict__",
    )
    for name in leaked_names:
        try:
            return getattr(context, name)
        except AttributeError:
            continue
    raise ContractViolation("TRUSTED_CONTEXT_AUTHORITY_OPAQUE")


def _attempt_context_slot_injection() -> None:
    forged = object.__new__(_TrustedRequestContextV3)
    for name, value in (
            ("requestId", "req1_" + "aa" * 16),
            ("authority", object()),
            ("registry", {}),
            ("gate", object()),
            ("token", object())):
        try:
            object.__setattr__(forged, name, value)
        except AttributeError:
            continue
        return
    raise ContractViolation("TRUSTED_CONTEXT_AUTHORITY_OPAQUE")


def _structural_authority_probe() -> bool:
    """Recompute that only the authority class can mutate authority state."""
    try:
        tree = ast.parse(pathlib.Path(__file__).read_text())
    except (OSError, UnicodeError, SyntaxError):
        return False

    class_nodes = {
        node.name: node for node in tree.body if isinstance(node, ast.ClassDef)
    }
    context_node = class_nodes.get("_TrustedRequestContextV3")
    authority_node = class_nodes.get("TrustedHostRequestAuthorityV3")
    if context_node is None or authority_node is None:
        return False

    context_methods = {
        node.name for node in context_node.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    if context_methods != {
            "__init__", "__copy__", "__deepcopy__", "__reduce__",
            "__reduce_ex__", "__getstate__", "__setstate__"}:
        return False
    slot_values = []
    for node in context_node.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "__slots__"
                for target in node.targets):
            slot_values.append(node.value)
    if len(slot_values) != 1 or not isinstance(slot_values[0], ast.Tuple) or \
            slot_values[0].elts:
        return False

    authority_methods = {
        node.name for node in authority_node.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    if not {"__init__", "begin", "internal_retry", "request_id"}.issubset(
            authority_methods):
        return False

    # Track lexical owners of assignments to self.__state.  No module helper,
    # context, or other class may bind or replace an authority's registry.
    state_write_owners: list[tuple[str | None, str | None]] = []

    class StateWriteVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.class_name: str | None = None
            self.function_name: str | None = None

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            previous = self.class_name
            self.class_name = node.name
            for child in node.body:
                self.visit(child)
            self.class_name = previous

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            previous = self.function_name
            self.function_name = node.name
            for child in node.body:
                self.visit(child)
            self.function_name = previous

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_Assign(self, node: ast.Assign) -> None:
            for target in node.targets:
                if isinstance(target, ast.Attribute) and \
                        isinstance(target.value, ast.Name) and \
                        target.value.id == "self" and \
                        target.attr == "__state":
                    state_write_owners.append(
                        (self.class_name, self.function_name))
            self.generic_visit(node.value)

        def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
            target = node.target
            if isinstance(target, ast.Attribute) and \
                    isinstance(target.value, ast.Name) and \
                    target.value.id == "self" and target.attr == "__state":
                state_write_owners.append((self.class_name, self.function_name))
            if node.value is not None:
                self.generic_visit(node.value)

    StateWriteVisitor().visit(tree)
    if not state_write_owners or any(
            owner[0] != "TrustedHostRequestAuthorityV3" or
            owner[1] not in {"__init__", "begin"}
            for owner in state_write_owners):
        return False

    banned_definitions = {
        "_MintGateV2", "_mint_context", "_request_id", "HostRequestIngressV2",
    }
    defined = {
        node.name for node in tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
    }
    if banned_definitions & defined or "_MINT_TOKEN" in globals():
        return False
    if any(isinstance(value, (TrustedHostRequestAuthorityV3,
                              _TrustedRequestContextV3))
           for value in globals().values()):
        return False
    return True


def _no_shared_authority_attack(
        selected: TrustedHostRequestAuthorityV3,
) -> None:
    if not _structural_authority_probe():
        return
    independent = TrustedHostRequestAuthorityV3()
    foreign = independent.begin("CLI", "req1_" + "77" * 16)
    try:
        selected.request_id(foreign)
    except ContractViolation as exc:
        if exc.code != "TRUSTED_CONTEXT_UNREGISTERED":
            raise
        raise ContractViolation("NO_SHARED_MINT_AUTHORITY") from exc


def _adversarial_source_execution_probe() -> tuple[bool, bool]:
    """Exercise the actual helper for malicious-pyc and wrong-hash cases."""
    import importlib.util
    import struct
    import tempfile
    import textwrap

    pyc_ignored = False
    wrong_hash_preexecution = False
    with tempfile.TemporaryDirectory(prefix="trc-v3-source-") as tmp:
        root = pathlib.Path(tmp)
        filename = "probe_dep.py"
        source_path = root / filename
        source_text = textwrap.dedent(
            '''
            BINDING = "operability.v2.json"
            def check(*args, **kwargs):
                return []
            ''').lstrip()
        source_raw = source_text.encode("utf-8")
        source_path.write_bytes(source_raw)
        expected = _sha_bytes(source_raw)

        marker = root / "pyc-marker.txt"
        malicious = textwrap.dedent(
            f'''
            BINDING = "operability.v2.json"
            open({str(marker)!r}, "w", encoding="utf-8").write("PYC_EXECUTED")
            def check(*args, **kwargs):
                return []
            ''').lstrip()
        evil_code = compile(
            malicious, str(source_path.resolve()), "exec", dont_inherit=True)
        header = importlib.util.MAGIC_NUMBER + struct.pack(
            "<III", 0, int(source_path.stat().st_mtime),
            source_path.stat().st_size)
        cache_dir = root / "__pycache__"
        cache_dir.mkdir()
        tag = f"cpython-{sys.version_info.major}{sys.version_info.minor}"
        (cache_dir / f"probe_dep.{tag}.pyc").write_bytes(
            header + marshal.dumps(evil_code))

        try:
            module = _exec_pinned_source(
                filename, expected, allow_local=frozenset({filename}), root=root)
            pyc_ignored = (
                getattr(module, "BINDING", None) == SOURCE_ARTIFACT and
                callable(getattr(module, "check", None)) and
                not marker.exists())
        except Exception:
            pyc_ignored = False

        wrong_marker = root / "wrong-hash-marker.txt"
        wrong_name = "wrong_hash.py"
        wrong_path = root / wrong_name
        wrong_path.write_text(
            f'open({str(wrong_marker)!r}, "w").write("EXECUTED")\n')
        try:
            _exec_pinned_source(
                wrong_name, "0" * 64,
                allow_local=frozenset({wrong_name}), root=root)
        except ValueError:
            wrong_hash_preexecution = not wrong_marker.exists()
        except Exception:
            wrong_hash_preexecution = False
    return pyc_ignored, wrong_hash_preexecution


def _capability_probes(
) -> tuple[dict[str, bool], dict[str, bool], dict[str, bool]]:
    selected = TrustedHostRequestAuthorityV3()
    second = TrustedHostRequestAuthorityV3()
    cli_id = "req1_" + "01" * 16
    api_id = "req1_" + "02" * 16
    recovery_id = "req1_" + "03" * 16
    foreign_id = "req1_" + "04" * 16
    unreserved_id = "req1_" + "05" * 16

    cli = selected.begin("CLI", cli_id)
    cli_state = _authority_state_fingerprint(selected)
    retry = selected.internal_retry(cli)
    retry_state = _authority_state_fingerprint(selected)
    api = selected.begin("API", api_id)
    recovery = selected.begin("recovery", recovery_id)
    foreign = second.begin("CLI", foreign_id)

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

    positive = {
        "TRC3-POS-01-CLI-EXACT-BINDING":
            type(cli) is _TrustedRequestContextV3 and
            selected.request_id(cli) == cli_id and
            _reservation_count(selected, cli_id) == 1,
        "TRC3-POS-02-INTERNAL-RETRY":
            retry is cli and selected.request_id(retry) == cli_id and
            cli_state == retry_state,
        "TRC3-POS-03-API-NEW-CONTEXT":
            api is not cli and selected.request_id(api) == api_id and
            _reservation_count(selected, api_id) == 1,
        "TRC3-POS-04-RECOVERY-NEW-CONTEXT":
            recovery is not cli and recovery is not api and
            selected.request_id(recovery) == recovery_id and
            _reservation_count(selected, recovery_id) == 1,
        "TRC3-POS-05-NONSERIALIZABLE":
            json_rejected and pickle_rejected and copy_rejected and
            deepcopy_rejected and
            REQUEST_RE.fullmatch(selected.request_id(cli)) is not None,
    }

    def retained(action: Callable[[], Any], code: str) -> bool:
        return _retained_negative(selected, action, code)

    negative = {
        "TRC3-NEG-01-RAW-STRING": retained(
            lambda: selected.request_id(cli_id), "TRUSTED_CONTEXT_REQUIRED"),
        "TRC3-NEG-02-PARSED-JSON": retained(
            lambda: selected.request_id({"requestId": cli_id}),
            "TRUSTED_CONTEXT_REQUIRED"),
        "TRC3-NEG-03-CALLER-CONSTRUCTION": retained(
            lambda: selected.request_id(_caller_construction_route()),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC3-NEG-04-SINK-CONSTRUCTION": retained(
            lambda: selected.request_id(_sink_construction_route()),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC3-NEG-05-PROVIDER-CONSTRUCTION": retained(
            lambda: selected.request_id(_provider_construction_route()),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC3-NEG-06-STAGE-CONSTRUCTION": retained(
            lambda: selected.request_id(_stage_construction_route()),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC3-NEG-07-PROFILE-CONSTRUCTION": retained(
            lambda: selected.request_id(_profile_construction_route()),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC3-NEG-08-PROJECTION-ADAPTER-CONSTRUCTION": retained(
            lambda: selected.request_id(
                _projection_adapter_construction_route()),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC3-NEG-09-UPPERCASE": retained(
            lambda: selected.begin("CLI", "req1_" + "AA" * 16),
            "REQUEST_ID_INVALID_REPRESENTATION"),
        "TRC3-NEG-10-UUID-ALIAS": retained(
            lambda: selected.begin(
                "CLI", "00000000-0000-0000-0000-000000000000"),
            "REQUEST_ID_INVALID_REPRESENTATION"),
        "TRC3-NEG-11-COLLISION-REUSE": retained(
            lambda: selected.begin("API", cli_id), "REQUEST_ID_COLLISION"),
        "TRC3-NEG-12-INTERNAL-REMINT": retained(
            lambda: selected.internal_retry(cli, "req1_" + "06" * 16),
            "INTERNAL_RETRY_CONTEXT_DRIFT"),
        "TRC3-NEG-13-EXTERNAL-CONTEXT-REUSE": retained(
            lambda: selected.begin("recovery", "req1_" + "07" * 16, cli),
            "NEW_INVOCATION_REQUIRES_NEW_CONTEXT"),
        "TRC3-NEG-14-CAPABILITY-SERIALIZATION": retained(
            lambda: cli.__reduce__(), "TRUSTED_CONTEXT_NONSERIALIZABLE"),
        "TRC3-NEG-15-SEMANTIC-PROJECTION": retained(
            lambda: _semantic_project(cli),
            "REQUEST_ID_SEMANTIC_EXCLUSION_VIOLATION"),
        "TRC3-NEG-16-OBJECT-NEW-FORGE": retained(
            lambda: selected.request_id(object.__new__(_TrustedRequestContextV3)),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC3-NEG-17-COPY": retained(
            lambda: copy.copy(cli), "TRUSTED_CONTEXT_NONCOPYABLE"),
        "TRC3-NEG-18-DEEPCOPY": retained(
            lambda: copy.deepcopy(cli), "TRUSTED_CONTEXT_NONCOPYABLE"),
        "TRC3-NEG-19-PICKLE-CONTEXT": retained(
            lambda: pickle.dumps(cli), "TRUSTED_CONTEXT_NONSERIALIZABLE"),
        "TRC3-NEG-20-UNPICKLE-LOOKALIKE": retained(
            lambda: selected.request_id(
                pickle.loads(pickle.dumps({"requestId": cli_id}))),
            "TRUSTED_CONTEXT_REQUIRED"),
        "TRC3-NEG-21-INDEPENDENT-AUTHORITY": retained(
            lambda: selected.request_id(foreign),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC3-NEG-22-POPULATED-REGISTRY-SUBSTITUTION": retained(
            lambda: _populated_registry_substitution(selected, cli_id),
            "TRUSTED_AUTHORITY_PARAMETER_FORBIDDEN"),
        "TRC3-NEG-23-NEW-GATE-AND-MINT-EQUIVALENT": retained(
            lambda: selected.request_id(
                TrustedHostRequestAuthorityV3().begin(
                    "CLI", "req1_" + "08" * 16)),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC3-NEG-24-NO-GLOBAL-SHARED-MINT-AUTHORITY": retained(
            lambda: _no_shared_authority_attack(selected),
            "NO_SHARED_MINT_AUTHORITY"),
        "TRC3-NEG-25-DIRECT-NO-INGRESS-ALLOCATION": retained(
            lambda: selected.request_id(object.__new__(_TrustedRequestContextV3)),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC3-NEG-26-CONTEXT-AUTHORITY-LEAK": retained(
            lambda: _attempt_context_authority_leak(cli),
            "TRUSTED_CONTEXT_AUTHORITY_OPAQUE"),
        "TRC3-NEG-27-DUPLICATE-CONTEXT": retained(
            lambda: _duplicate_context_attack(selected, cli_id),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC3-NEG-28-UNRESERVED-CONTEXT": retained(
            lambda: _unreserved_context_attack(selected, unreserved_id),
            "TRUSTED_CONTEXT_UNREGISTERED"),
        "TRC3-NEG-29-CALLER-REGISTRY-ARGUMENT": retained(
            lambda: selected.request_id(cli, {cli_id: (1, cli)}),
            "TRUSTED_AUTHORITY_PARAMETER_FORBIDDEN"),
        "TRC3-NEG-30-CONTEXT-SLOT-INJECTION": retained(
            _attempt_context_slot_injection,
            "TRUSTED_CONTEXT_AUTHORITY_OPAQUE"),
    }

    pyc_ignored, wrong_hash_preexecution = _adversarial_source_execution_probe()
    advanced = {
        "TRC3-ADV-01-ACTUAL-HELPER-PYC-IGNORED": pyc_ignored,
        "TRC3-ADV-02-ACTUAL-HELPER-WRONG-HASH-PREEXECUTION":
            wrong_hash_preexecution,
        "TRC3-ADV-03-STRUCTURAL-AUTHORITY-ROOT":
            _structural_authority_probe(),
        "TRC3-ADV-04-CONTEXT-FIELDLESS":
            _TrustedRequestContextV3.__slots__ == () and
            not hasattr(cli, "__dict__"),
        "TRC3-ADV-05-SECOND-AUTHORITY-STATE-INDEPENDENT":
            _reservation_count(second, foreign_id) == 1 and
            _reservation_count(selected, foreign_id) is None,
        "TRC3-ADV-06-DISTINCT-CONSTRUCTION-ROUTES":
            len({id(route.__code__) for route in (
                _caller_construction_route,
                _sink_construction_route,
                _provider_construction_route,
                _stage_construction_route,
                _profile_construction_route,
                _projection_adapter_construction_route,
            )}) == 6 and all(
                {"object", "__new__", "_TrustedRequestContextV3"}.issubset(
                    set(route.__code__.co_names))
                for route in (
                    _caller_construction_route,
                    _sink_construction_route,
                    _provider_construction_route,
                    _stage_construction_route,
                    _profile_construction_route,
                    _projection_adapter_construction_route,
                )),
    }
    return positive, negative, advanced


def _load_process_inputs() -> tuple[Any | None, Any | None, list[str]]:
    errors: list[str] = []
    predecessor: Any | None = None
    rejection: Any | None = None
    try:
        predecessor = _read_json(HERE / PREDECESSOR)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError,
            TypeError, ValueError) as exc:
        errors.append(
            "TRC3-DELTA: predecessor could not be decoded "
            f"({type(exc).__name__})")
    try:
        rejection = _read_json(HERE / REJECTION)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError,
            TypeError, ValueError) as exc:
        errors.append(
            "TRC3-REVIEW: v2 rejection could not be decoded "
            f"({type(exc).__name__})")
    return predecessor, rejection, errors


def _review_finding_ids(rejection: Any) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    if not isinstance(rejection, dict):
        return set(), ["TRC3-REVIEW: v2 rejection root is not an object"]
    verdict = rejection.get("verdict")
    if not isinstance(verdict, dict) or verdict.get("decision") != "REJECT" or \
            verdict.get("disposition") != "REJECT-EXACT-BYTES" or \
            verdict.get("independentAcceptance") is not False:
        errors.append("TRC3-REVIEW: frozen v2 rejection verdict drift")
    rows: list[Any] = []
    for key in ("blockingFindings", "checkerCoverageObservations"):
        value = rejection.get(key)
        if not isinstance(value, list):
            errors.append(f"TRC3-REVIEW: {key} is not a list")
            continue
        rows.extend(value)
    identities: list[str] = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            errors.append("TRC3-REVIEW: finding/observation identity malformed")
            continue
        identities.append(row["id"])
    if len(identities) != len(set(identities)):
        errors.append("TRC3-REVIEW: duplicate v2 finding identity")
    return set(identities), errors


def _check(value: Any, *, verify_files: bool) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["TRC3-TOTALITY-ROOT: contract root must be an object"]

    source, source_errors = _load_source(verify_files=verify_files)
    errors.extend(source_errors)
    predecessor, rejection, process_errors = _load_process_inputs()
    errors.extend(process_errors)

    if not isinstance(predecessor, dict):
        errors.append("TRC3-DELTA: predecessor root is not an object")
    else:
        expected_root = set(predecessor) | ADDED_ROOT_KEYS
        if set(value) != expected_root:
            errors.append("TRC3-SCHEMA: root field set differs from closed delta")
        for key in set(predecessor) - CHANGED_ROOT_KEYS:
            if value.get(key) != predecessor.get(key):
                errors.append(f"TRC3-DELTA: unlisted predecessor root changed: {key}")
        for key in PROTECTED_ROOT_KEYS:
            if value.get(key) != predecessor.get(key):
                errors.append(f"TRC3-DELTA: protected predecessor root changed: {key}")

    exact_scalars = {
        "artifact": "opensip.trusted-request-context",
        "version": 3,
        "date": "2026-08-01",
        "status": "CANDIDATE-NOT-APPLIED",
        "reviewStatus": "AWAITING-INDEPENDENT-REVIEW",
        "sealRecommendation": "DO-NOT-SEAL-OR-APPLY",
    }
    for key, expected in exact_scalars.items():
        if value.get(key) != expected:
            errors.append(f"TRC3-SCHEMA: {key} drift")

    if value.get("successorDelta") != SUCCESSOR_DELTA:
        errors.append("TRC3-DELTA: closed v3-to-v2 declaration drift")
    for key, expected_digest in CHANGED_SECTION_SHA256.items():
        try:
            observed = _canonical_digest(value.get(key))
        except (TypeError, ValueError) as exc:
            errors.append(
                f"TRC3-SCHEMA: {key} is not canonical JSON "
                f"({type(exc).__name__})")
            continue
        if observed != expected_digest:
            errors.append(f"TRC3-SCHEMA: closed {key} value drift")

    if source is not None:
        try:
            expected_projection = _extract_source(source)
        except (AttributeError, IndexError, KeyError, TypeError,
                ValueError) as exc:
            errors.append(
                "TRC3-SOURCE: closed source extraction failed "
                f"({type(exc).__name__})")
        else:
            if value.get("sourceProjection") != expected_projection:
                errors.append(
                    "TRC3-SOURCE: sourceProjection is not exact OP2 recomputation")

    # Denominators and typed outcomes are checker-owned, not accepted from the
    # candidate's authored lists.
    positive_rows = value.get("positiveControls")
    if not isinstance(positive_rows, list) or any(
            not isinstance(row, dict) for row in positive_rows):
        errors.append("TRC3-SCHEMA: positive control rows malformed")
    else:
        authored_positive = tuple(row.get("id") for row in positive_rows)
        if authored_positive != POSITIVE_IDS:
            errors.append("TRC3-PROBE: positive control denominator drift")

    negative_rows = value.get("adversarialControls")
    if not isinstance(negative_rows, list) or any(
            not isinstance(row, dict) for row in negative_rows):
        errors.append("TRC3-SCHEMA: adversarial control rows malformed")
    else:
        authored_negative = tuple(
            (row.get("id"), row.get("expected")) for row in negative_rows)
        if authored_negative != NEGATIVE_CODES:
            errors.append("TRC3-PROBE: adversarial denominator/code drift")

    required_v2_ids, review_errors = _review_finding_ids(rejection)
    errors.extend(review_errors)
    disposition_rows = value.get("findingDispositions")
    if not isinstance(disposition_rows, list) or any(
            not isinstance(row, dict) for row in disposition_rows):
        errors.append("TRC3-REVIEW: finding dispositions malformed")
    else:
        disposition_ids = [row.get("id") for row in disposition_rows]
        if len(disposition_ids) != len(set(disposition_ids)):
            errors.append("TRC3-REVIEW: duplicate finding disposition")
        required_ids = required_v2_ids | {
            "TRC-PF-01-UNPINNED-PYC-EXECUTION",
            "TRC-PF-02-CAPABILITY-ORACLE-FORGEABLE",
        }
        if set(disposition_ids) != required_ids:
            errors.append(
                "TRC3-REVIEW: v1/v2 rejection disposition closure drift")

    positive, negative, advanced = _capability_probes()
    failed_positive = [key for key, passed in positive.items() if not passed]
    failed_negative = [key for key, passed in negative.items() if not passed]
    failed_advanced = [key for key, passed in advanced.items() if not passed]
    if tuple(positive) != POSITIVE_IDS or failed_positive:
        errors.append(
            "TRC3-PROBE: positive controls failed: " +
            ",".join(failed_positive or ["denominator-drift"]))
    if tuple(negative) != tuple(key for key, _ in NEGATIVE_CODES) or \
            failed_negative:
        errors.append(
            "TRC3-PROBE: adversarial controls failed: " +
            ",".join(failed_negative or ["denominator-drift"]))
    if failed_advanced:
        errors.append(
            "TRC3-PROBE: advanced controls failed: " +
            ",".join(failed_advanced))
    return errors


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    """Total parsed-JSON boundary: malformed shapes become findings."""
    try:
        return _check(value, verify_files=verify_files)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError,
            RuntimeError) as exc:
        return [
            "TRC3-TOTALITY-EXCEPTION: malformed contract shape "
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


def _append(path: tuple[Any, ...], value_to_add: Any) -> Callable[[Any], None]:
    def mutate(value: Any) -> None:
        target = value
        for key in path:
            target = target[key]
        target.append(value_to_add)
    return mutate


def _add_unknown(value: Any) -> None:
    value["unknownAuthority"] = True


MUTATIONS: list[tuple[str, Callable[[Any], None]]] = [
    ("version rollback", _set(("version",), 2)),
    ("application status", _set(("status",), "APPLIED")),
    ("self review", _set(("reviewStatus",), "PASS")),
    ("seal recommendation", _set(("sealRecommendation",), "SEAL")),
    ("unknown root", _add_unknown),
    ("drop successor delta", _drop(("successorDelta",))),
    ("predecessor pin", _set(("successorDelta", "predecessor"), "v2@bad")),
    ("rejection pin", _set(("successorDelta", "rejection"), "review@bad")),
    ("omit changed dependency closure", _drop(
        ("successorDelta", "changedRootKeys", 3))),
    ("add undeclared root", _append(
        ("successorDelta", "addedRootKeys"), "authorityToken")),
    ("remove protected source", _drop(
        ("successorDelta", "protectedRootKeys", 4))),
    ("purpose weakens authority", _set(("purpose",), "context is authority")),
    ("context carries request id", _set(
        ("capabilityContract", "contextExposes"), ["requestId"])),
    ("context supplies authority", _set(
        ("capabilityContract", "authorityRegistry", "contextSuppliedAuthority"),
        True)),
    ("caller registry accepted", _set(
        ("capabilityContract", "authorityRegistry", "callerSuppliedRegistry"),
        True)),
    ("public constructor", _set(
        ("capabilityContract", "publicConstructors"), ["from_string"])),
    ("serializable", _set(("capabilityContract", "serializable"), True)),
    ("copyable", _set(("capabilityContract", "copyable"), True)),
    ("mint owner caller", _set(
        ("capabilityContract", "mintOwner"), "caller")),
    ("remove exact object rule", _set(
        ("capabilityContract", "authorityRegistry", "value"),
        "any structurally equal context")),
    ("projection takes gate", _set(
        ("capabilityContract", "allowedProjection", "method"),
        "request_id(context, gate)")),
    ("projection adds authority", _set(
        ("capabilityContract", "allowedProjection", "fields"),
        ["requestId", "authority"])),
    ("global helper allowed", _set(
        ("capabilityContract", "tokenRule"),
        "A global mint helper is allowed.")),
    ("remove stage route", _drop(
        ("capabilityContract", "forbiddenConstructionSources", 5))),
    ("retry remints", _set(
        ("invocationLifecycle", "internalRetry"), "mint again")),
    ("new invocation reuses", _set(
        ("invocationLifecycle", "newInvocation"), "reuse prior context")),
    ("drop source successor input", _drop(
        ("dependencyClosure", "successorInputs", 6))),
    ("add E8 back edge", _append(
        ("dependencyClosure", "data"), "evidence.v8.json")),
    ("source projection drift", _set(
        ("sourceProjection", "authority", "allocationOwner"), "caller")),
    ("source representation drift", _set(
        ("sourceProjection", "representation", "regex"), ".*")),
    ("drop positive", _drop(("positiveControls", 0))),
    ("rename positive", _set(("positiveControls", 0, "id"), "PRESENT")),
    ("drop stage negative", _drop(("adversarialControls", 5))),
    ("weaken substitution expected", _set(
        ("adversarialControls", 21, "expected"), "TYPE_ERROR")),
    ("drop no-ingress negative", _drop(("adversarialControls", 24))),
    ("change construction denominator", _set(
        ("adversarialControls", 7, "id"), "TRC3-NEG-08-GENERIC")),
    ("drop authority invariant", _drop(("invariants", 1))),
    ("drop exact-helper invariant", _drop(("invariants", 6))),
    ("claim runtime executed", _set(
        ("assurance", "runtimeImplementationExecuted"), True)),
    ("claim product qualified", _set(
        ("assurance", "productQualified"), True)),
    ("drop independent review", _drop(("retainedResiduals", 0))),
    ("drop production residual", _drop(("retainedResiduals", 1))),
    ("drop atomic residual", _drop(("retainedResiduals", 2))),
    ("drop same-process boundary", _drop(("retainedResiduals", 3))),
    ("drop v1 pyc disposition", _drop(("findingDispositions", 0))),
    ("drop v1 forge disposition", _drop(("findingDispositions", 1))),
    ("drop v2 blocker disposition", _drop(("findingDispositions", 2))),
    ("drop registry observation", _drop(("findingDispositions", 3))),
    ("claim repaired in v2", _set(
        ("findingDispositions", 1, "disposition"),
        "ACCEPTED-AND-REPAIRED-IN-V2")),
    ("source pin drift", _set(("sourceAuthority", "sha256"), "0" * 64)),
]


TOTALITY_CASES: list[tuple[str, Any]] = [
    ("null", None),
    ("string", "context"),
    ("number", 7),
    ("array", []),
    ("empty object", {}),
    ("nested scalar", {"successorDelta": 1}),
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
        except (AttributeError, IndexError, KeyError, TypeError,
                ValueError) as exc:
            escaped += 1
            print(
                f"  ESCAPE  {label} (mutation failed: {type(exc).__name__})")
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
    print(
        f"  {'reject' if duplicate_rejected else 'ESCAPE':>6}  duplicate JSON key")

    denominator = len(TOTALITY_CASES) + len(MUTATIONS) + 1
    if escaped:
        print(f"{escaped}/{denominator} retained selftest cases ESCAPED")
        return 1
    print(
        f"all {len(MUTATIONS)} mutations, {len(TOTALITY_CASES)} totality "
        "cases, and 1 duplicate-key case rejected")
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
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError,
            TypeError, ValueError) as exc:
        print(f"1 finding(s) in {path.name}:")
        print(f"  - TRC3-TOTALITY-DECODE: {type(exc).__name__}")
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
        f"trusted request context v3 OK — {path.name}; exact OP2 projection; "
        "independently rooted authority; exact reservation-to-object binding; "
        f"{len(POSITIVE_IDS)} positive and {len(NEGATIVE_CODES)} adversarial "
        "controls")
    print(
        "  assurance: trusted-host API/provenance model; "
        "IMPLEMENTABLE_UNEXECUTED; AWAITING-INDEPENDENT-REVIEW; NOT APPLIED; "
        "DO-NOT-SEAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
