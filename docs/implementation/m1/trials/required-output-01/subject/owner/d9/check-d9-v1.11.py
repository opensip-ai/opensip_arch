#!/usr/bin/env python3
"""Complete frozen-RT14 compatibility successor for D9 v1.11.

v1.11 projects exactly to rejected v1.10 and changes no D9 taxonomy,
derivation, reducer, golden, identity, generic-scope, or remedy semantics.  It
repairs v1.10's incomplete consumer-surface claim by deriving every D9 access
from the pinned RT14 checker AST, restoring the authenticated ``V17`` module
chain, and exposing RT14's exact three-argument ``check`` adapter.

All predecessor and consumer bytes are read and hash-verified before any
retained executable source is compiled.  The public ``check`` function is the
v1.8 compatibility API consumed by RT14; this candidate's own closed-successor
validation is deliberately private as ``_check_contract``.

Usage: python3 -B artifacts/check-d9-v1.11.py [contract] [--selftest]
Exit: 0 clean · 1 findings/pin rejection · 2 input/JSON error
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.machinery
import importlib.util
import inspect
import json
import marshal
import pathlib
import shutil
import struct
import subprocess
import sys
import tempfile
import types
from typing import Any, Callable, Mapping


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "d9-exit-contract.v1.11.json"
CHECKER = "check-d9-v1.11.py"
PREDECESSOR = "d9-exit-contract.v1.10.json"
PREDECESSOR_CHECKER = "check-d9-v1.10.py"
PREDECESSOR_REVIEW = \
    "d9-exit-contract.v1.10.review-independent-prefreeze.json"
V19 = "d9-exit-contract.v1.9.json"
V19_CHECKER = "check-d9-v1.9.py"
V19_REVIEW = "d9-exit-contract.v1.9.review-independent-prefreeze.json"
V18 = "d9-exit-contract.v1.8.json"
V18_CHECKER = "check-d9-v1.8.py"
V18_REVIEW = "d9-exit-contract.v1.8.review-independent-prefreeze.json"
V17_DATA = "d9-exit-contract.v1.7.json"
V17_CHECKER = "check-d9-v1.7.py"
V16_DATA = "d9-exit-contract.v1.6.json"
V16_CHECKER = "check-d9.py"
RT14 = "retention-tiers.v14.json"
RT14_CHECKER = "check-retention-custody-v14.py"
RT14_REVIEW = "retention-tiers.v14.review-independent-prefreeze.json"

EXPECTED_VERSION = "v1.11"
EXPECTED_STATUS = (
    "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW "
    "(v1.11 complete frozen-RT14 checker-surface repair over rejected v1.10)"
)
EXPECTED_PURPOSE = (
    "Total host-owned process-exit contract: preserve every v1.10 semantic and "
    "trust-boundary repair while restoring the complete public checker surface "
    "mechanically derived from frozen RT14, including its exact three-argument "
    "check adapter and authenticated V17.V16.derive_class chain."
)
REFERENCE_IMPLEMENTATION = (
    "artifacts/check-d9-v1.11.py::"
    "check+derive_class+derive_codes+reduce_concurrent+V17.V16.derive_class"
)
REPRODUCE = (
    "python3 -B artifacts/check-d9-v1.11.py         # defaults to the binding "
    "v1.11 artifact"
)
MUTATION_PROOF = (
    "python3 -B artifacts/check-d9-v1.11.py --selftest  # retains all "
    "v1.10/v1.9/v1.8/v1.7/v1.6 proofs; rejects AST-surface, V17-chain, "
    "three-argument-check, trust-order and compatibility mutations; and runs "
    "a disposable RT14 checker-API compatibility probe normal plus selftest"
)
EXPECTED_CLAIM = (
    "Every v1.10 semantic result is retained exactly; the complete frozen RT14 "
    "D9 call surface is enumerated from its pinned AST, resolved and invoked "
    "against authenticated predecessor modules, and exercised end-to-end by a "
    "disposable RT14 checker-API compatibility probe."
)
COMPATIBILITY_KEY = "v110CompatibilityDisposition"
REJECTION_ID = "D9V110-PF-01-INCOMPLETE-CONSUMER-SURFACE"

INHERITED_PINS: dict[str, str] = {
    V19: "bc3c2b48d3615bc262166a698d3a3559bc2fa2fbd2f637de0dbf943309194404",
    V19_CHECKER: "956e41e279e758af5dd5e342a5404f334f6223add72abdb1340c85fafa2bd936",
    V19_REVIEW: "409e55ddcc2121da5624a112728cd2d126586411a9abe06435c64d1c02b71373",
    V18: "5fb5466372da7c8ef935a1233eb67869f21c3cdb21d67b3767159998ad26a30d",
    V18_CHECKER: "827e5bdd600e2682d7653bc738f07efe066f90f4d7db7bad16a7f7fd5eb91e47",
    V18_REVIEW: "f044620aaac0ea4f7efc6bdd51983278bf5858f5f967b6d48310e7c0139fedb9",
    V17_DATA: "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    V17_CHECKER: "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
    V16_DATA: "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    V16_CHECKER: "9f8e16a0000e59d2f1326f97f1b8afcc5c7121eb0c57b6c440d76b9c401346a7",
    RT14: "b66d0275d326cdd0cfdbec5e0810788e7768c10c9f1d7ab2c4df8c44b6975770",
    RT14_CHECKER: "6b190a89ba1700cf820746b473e8e3a521c9b2f6b4856f0c501d72a44b0a1d60",
    RT14_REVIEW: "dfb037bd121f7b73fbfeb77bbbaf0e1028a8c89318c5991bb3b3ec935046575c",
}
PINS: dict[str, str] = {
    PREDECESSOR: "bf1d7eb0ab24de89f665f46c25377195a2721fc7fcb62f3aa449d0887b705b7b",
    PREDECESSOR_CHECKER: "77f86334a0ee016960224880fe75ef2b9b44d3adf20799c8354e992fbf19cca6",
    PREDECESSOR_REVIEW: "7faefdf8f2c19e39ad9fdd6fba8df6f08c586aa73b7e5ab7ed917ae4c223e476",
    **INHERITED_PINS,
}
ROLES = {
    PREDECESSOR: "rejected v1.10 candidate projected exactly for retained checks",
    PREDECESSOR_CHECKER: "retained executable v1.10 checker",
    PREDECESSOR_REVIEW: "independent v1.10 rejection and repair authority",
    V19: "independently passed retained predecessor data",
    V19_CHECKER: "retained executable v1.9 checker",
    V19_REVIEW: "independent narrow PASS authority for v1.9",
    V18: "retained v1.8 compatibility data consumed unchanged by RT14",
    V18_CHECKER: "authenticated compatibility implementation",
    V18_REVIEW: "independent v1.8 rejection authority",
    V17_DATA: "authenticated public-check predecessor data",
    V17_CHECKER: "authenticated V17 module restored as public namespace",
    V16_DATA: "authenticated retained v1.6 data",
    V16_CHECKER: "authenticated V16 module behind V17.V16",
    RT14: "inert frozen consumer contract",
    RT14_CHECKER: "inert frozen consumer source used for AST surface derivation",
    RT14_REVIEW: "consumer review and fork guard",
}

EXPECTED_CALL_SITES = [
    {"line": 357, "path": "derive_class", "positionalArity": 1,
     "keywordNames": []},
    {"line": 358, "path": "derive_codes", "positionalArity": 2,
     "keywordNames": []},
    {"line": 472, "path": "V17.V16.derive_class", "positionalArity": 1,
     "keywordNames": []},
    {"line": 473, "path": "derive_class", "positionalArity": 1,
     "keywordNames": []},
    {"line": 480, "path": "reduce_concurrent", "positionalArity": 2,
     "keywordNames": []},
    {"line": 534, "path": "check", "positionalArity": 3,
     "keywordNames": []},
]
TOP_LEVEL_EXPORTS = [
    {"name": "check", "kind": "callable", "positionalArity": 3},
    {"name": "derive_class", "kind": "callable", "positionalArity": 1},
    {"name": "derive_codes", "kind": "callable", "positionalArity": 2},
    {"name": "reduce_concurrent", "kind": "callable", "positionalArity": 2},
    {"name": "V17", "kind": "module"},
]
CHAINED_EXPORTS = [
    {"path": "V17.V16", "kind": "module"},
    {"path": "V17.V16.derive_class", "kind": "callable",
     "positionalArity": 1},
]


class DuplicateKeyError(ValueError):
    pass


class AuthorityLoadError(RuntimeError):
    pass


class PinMismatch(AuthorityLoadError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def _parse_json_bytes(source: bytes, name: str) -> Any:
    try:
        return json.loads(source.decode("utf-8"), object_pairs_hook=_pairs)
    except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise AuthorityLoadError(
            f"cannot parse pinned data {name}: {type(exc).__name__}: {exc}"
        ) from exc


def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(), object_pairs_hook=_pairs)


class _VerifiedSourceLoader:
    """Execute one immutable already-verified source snapshot."""

    def __init__(self, filename: pathlib.Path, source: bytes):
        self.filename = filename
        self.source = source

    def create_module(self, _spec: Any) -> None:
        return None

    def exec_module(self, module: types.ModuleType) -> None:
        exec(compile(self.source, str(self.filename), "exec"), module.__dict__)


def _execute_snapshot(name: str, filename: str,
                      source: bytes) -> types.ModuleType:
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


def _execute_verified_v110(
        snapshots: Mapping[str, bytes], _parsed: Mapping[str, Any]
) -> tuple[types.ModuleType, Any]:
    """Build v1.10 authority using only the already-verified closure."""
    module = _execute_snapshot(
        "opensip_check_d9_v110_verified", PREDECESSOR_CHECKER,
        snapshots[PREDECESSOR_CHECKER])
    if dict(getattr(module, "PINS", {})) != INHERITED_PINS:
        raise AuthorityLoadError("v1.10 executable transitive pin set drifted")
    subset = {name: snapshots[name] for name in module.PINS}
    parsed = module.DeferredAuthorityLoader._parsed(subset)
    v19_checker, v19_authority = module._execute_verified_v19(subset, parsed)
    authority = module.Authority(
        snapshots=subset,
        predecessor=parsed[module.PREDECESSOR],
        predecessor_review=parsed[module.PREDECESSOR_REVIEW],
        rt14=parsed[module.RT14],
        rt14_review=parsed[module.RT14_REVIEW],
        v19_checker=v19_checker,
        v19_authority=v19_authority,
    )
    return module, authority


class Authority:
    """Plain immutable-by-convention record compatible with RT14's loader.

    Frozen RT14 executes dependencies without first registering them in
    ``sys.modules``.  ``dataclasses`` consults that registry while decorating a
    class on Python 3.14, so using it here would make an otherwise valid public
    checker fail at the consumer's import boundary.
    """

    def __init__(self, *, snapshots: Mapping[str, bytes],
                 predecessor: dict[str, Any],
                 predecessor_review: dict[str, Any],
                 rt14: dict[str, Any], rt14_review: dict[str, Any],
                 v18: dict[str, Any], v17: dict[str, Any],
                 v16: dict[str, Any], v110_checker: types.ModuleType,
                 v110_authority: Any, v18_checker: types.ModuleType,
                 v17_checker: types.ModuleType,
                 v16_checker: types.ModuleType):
        self.snapshots = snapshots
        self.predecessor = predecessor
        self.predecessor_review = predecessor_review
        self.rt14 = rt14
        self.rt14_review = rt14_review
        self.v18 = v18
        self.v17 = v17
        self.v16 = v16
        self.v110_checker = v110_checker
        self.v110_authority = v110_authority
        self.v18_checker = v18_checker
        self.v17_checker = v17_checker
        self.v16_checker = v16_checker


ReadBytes = Callable[[pathlib.Path], bytes]
ImportCallback = Callable[[Mapping[str, bytes], Mapping[str, Any]], Any]


class DeferredAuthorityLoader:
    """Read and verify the complete closure before any retained execution."""

    def __init__(self, directory: pathlib.Path = HERE):
        self.directory = directory

    def _snapshots(self, byte_reader: ReadBytes | None = None) -> dict[str, bytes]:
        reader = byte_reader or (lambda path: path.read_bytes())
        snapshots: dict[str, bytes] = {}
        errors: list[str] = []
        for name, expected in PINS.items():
            try:
                source = reader(self.directory / name)
            except (OSError, TypeError, ValueError) as exc:
                errors.append(f"{name}: read {type(exc).__name__}: {exc}")
                continue
            if not isinstance(source, bytes):
                errors.append(f"{name}: byte reader returned {type(source).__name__}")
                continue
            actual = hashlib.sha256(source).hexdigest()
            if actual != expected:
                errors.append(f"{name}: {actual} != {expected}")
            snapshots[name] = source
        if errors:
            raise PinMismatch("; ".join(errors))
        if set(snapshots) != set(PINS):
            raise PinMismatch("not every transitive input produced a snapshot")
        return snapshots

    @staticmethod
    def _parsed(snapshots: Mapping[str, bytes]) -> dict[str, Any]:
        parsed = {
            name: _parse_json_bytes(snapshots[name], name)
            for name in PINS if name.endswith(".json")
        }
        review = parsed[PREDECESSOR_REVIEW]
        verdict = review.get("verdict") if isinstance(review, dict) else None
        if not isinstance(verdict, dict) or verdict.get("decision") != "REJECT" or \
                verdict.get("blockingFindingCount") != 1 or \
                verdict.get("inputHashDrift") is not False:
            raise AuthorityLoadError("pinned v1.10 review is not the exact REJECT")
        window = review.get("hashWindow") or {}
        expected_window = {
            PREDECESSOR: PINS[PREDECESSOR],
            PREDECESSOR_CHECKER: PINS[PREDECESSOR_CHECKER],
            **INHERITED_PINS,
        }
        if window.get("startEqualsEnd") is not True or \
                window.get("inputHashDrift") is not False or \
                window.get("hashes") != expected_window:
            raise AuthorityLoadError("v1.10 review hash window does not bind all inputs")
        blockers = [
            row.get("id") for row in review.get("blockingFindings", [])
            if isinstance(row, dict)
        ]
        if blockers != [REJECTION_ID]:
            raise AuthorityLoadError("v1.10 review blocker drifted")
        return parsed

    def invoke_verified(self, callback: ImportCallback,
                        byte_reader: ReadBytes | None = None
                        ) -> tuple[Mapping[str, bytes], Mapping[str, Any], Any]:
        snapshots = self._snapshots(byte_reader)
        parsed = self._parsed(snapshots)
        result = callback(snapshots, parsed)
        return snapshots, parsed, result

    def load(self) -> Authority:
        snapshots, parsed, loaded = self.invoke_verified(_execute_verified_v110)
        if not isinstance(loaded, tuple) or len(loaded) != 2 or \
                not isinstance(loaded[0], types.ModuleType):
            raise AuthorityLoadError("verified importer did not return v1.10 authority")
        v110_checker, v110_authority = loaded
        try:
            v18_checker = v110_authority.v19_authority.v18_checker
            v17_checker = v18_checker.V17
            v16_checker = v17_checker.V16
        except AttributeError as exc:
            raise AuthorityLoadError("authenticated V17/V16 chain absent") from exc
        if not all(isinstance(item, types.ModuleType) for item in (
                v18_checker, v17_checker, v16_checker)) or \
                not callable(getattr(v16_checker, "derive_class", None)):
            raise AuthorityLoadError("authenticated V17/V16 chain has wrong runtime shape")
        return Authority(
            snapshots=snapshots,
            predecessor=parsed[PREDECESSOR],
            predecessor_review=parsed[PREDECESSOR_REVIEW],
            rt14=parsed[RT14],
            rt14_review=parsed[RT14_REVIEW],
            v18=parsed[V18],
            v17=parsed[V17_DATA],
            v16=parsed[V16_DATA],
            v110_checker=v110_checker,
            v110_authority=v110_authority,
            v18_checker=v18_checker,
            v17_checker=v17_checker,
            v16_checker=v16_checker,
        )


# RT14 resolves V17 during ordinary function execution immediately after module
# import.  Bootstrap eagerly, but only through the verified closure above.
_BOOTSTRAP_AUTHORITY = DeferredAuthorityLoader().load()
V17 = _BOOTSTRAP_AUTHORITY.v17_checker


def derive_class(ax: dict[str, Any]) -> str:
    """Delegate to authenticated v1.10 semantics."""
    return _BOOTSTRAP_AUTHORITY.v110_checker.derive_class(ax)


def derive_codes(ax: dict[str, Any], maps: dict[str, Any]) -> dict[str, Any]:
    """Delegate to authenticated v1.10 semantics."""
    return _BOOTSTRAP_AUTHORITY.v110_checker.derive_codes(ax, maps)


def reduce_concurrent(conditions: dict[str, Any],
                      precedence: list[str]) -> dict[str, Any]:
    """Delegate to authenticated v1.10's v1.8-equivalent reducer."""
    return _BOOTSTRAP_AUTHORITY.v110_checker.reduce_concurrent(
        conditions, precedence)


def check(candidate: object, predecessor: object, v16: object) -> list[str]:
    """Exact frozen-RT14 three-argument compatibility adapter.

    The authority arguments must be byte-semantically equal to the pinned v1.7
    and v1.6 snapshots.  This public function intentionally does not validate
    the v1.11 successor artifact; the CLI uses ``_check_contract`` for that.
    """
    authority = _BOOTSTRAP_AUTHORITY
    if not isinstance(predecessor, dict) or predecessor != authority.v17:
        return ["D30-COMPAT-AUTHORITY: predecessor is not pinned v1.7 data"]
    if not isinstance(v16, dict) or v16 != authority.v16:
        return ["D30-COMPAT-AUTHORITY: retained input is not pinned v1.6 data"]
    return authority.v18_checker.check(candidate, predecessor, v16)


def _rt14_path(node: ast.AST) -> str | None:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    rooted = isinstance(current, ast.Name) and current.id == "d9mod"
    if isinstance(current, ast.Subscript) and \
            isinstance(current.value, ast.Name) and \
            current.value.id == "authorities":
        slice_value = current.slice
        rooted = isinstance(slice_value, ast.Constant) and \
            slice_value.value == "d9mod"
    if not rooted or not parts:
        return None
    return ".".join(reversed(parts))


def _enumerate_rt14_calls(source: bytes) -> list[dict[str, Any]]:
    try:
        tree = ast.parse(source.decode("utf-8"), filename=RT14_CHECKER)
    except (UnicodeError, SyntaxError) as exc:
        raise AuthorityLoadError(
            f"cannot parse pinned RT14 consumer AST: {type(exc).__name__}"
        ) from exc
    rows: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        path = _rt14_path(node.func)
        if path is None:
            continue
        rows.append({
            "line": node.lineno,
            "path": path,
            "positionalArity": len(node.args),
            "keywordNames": [
                keyword.arg if keyword.arg is not None else "**"
                for keyword in node.keywords
            ],
        })
    return sorted(rows, key=lambda row: (row["line"], row["path"]))


def _consumer_surface(authority: Authority) -> dict[str, Any]:
    calls = _enumerate_rt14_calls(authority.snapshots[RT14_CHECKER])
    return {
        "source": RT14_CHECKER,
        "sourceSha256": PINS[RT14_CHECKER],
        "derivation": (
            "Parse the pinned Python source with ast; enumerate every Call whose "
            "receiver is d9mod or authorities['d9mod']; retain its full chained "
            "attribute path, source line, positional arity and keyword names."
        ),
        "receiverRoots": ["d9mod", "authorities['d9mod']"],
        "callSites": calls,
        "requiredTopLevelExports": copy.deepcopy(TOP_LEVEL_EXPORTS),
        "requiredChainedExports": copy.deepcopy(CHAINED_EXPORTS),
        "closureRule": (
            "Every AST-derived call path must resolve at runtime; each callable "
            "is invoked with its frozen-consumer arity. A predecessor-diff or "
            "declared-list-presence check is not a consumer-surface proof."
        ),
    }


def _trust_contract() -> dict[str, Any]:
    return {
        "id": "D9-V111-HASH-BEFORE-EXECUTION",
        "transitiveInputs": [
            {"path": name, "sha256": digest, "role": ROLES[name]}
            for name, digest in PINS.items()
        ],
        "requiredOrder": [
            "read every transitive input as inert bytes",
            "verify every byte snapshot against its pinned SHA-256 and abort the whole load on any mismatch",
            "parse pinned data snapshots and validate the exact v1.10 REJECT review/hash window without importing executable dependencies",
            "only after every pin and pinned-review verdict/binding is clean invoke the injectable authority-import callback",
            "compile and execute only already-verified checker byte snapshots; expose V17 only from the authenticated v1.8-to-v1.7-to-v1.6 module chain",
        ],
        "failureRule": (
            "Any transitive read, pin, data-snapshot parse, or pinned-review "
            "verdict/binding failure prevents the authority-import callback from "
            "being invoked and prevents V17 publication."
        ),
        "probe": (
            "The v1.11 selftest corrupts every pinned input with an import marker; "
            "each mismatch must be reported and every marker count remain zero."
        ),
    }


def _compatibility_disposition(authority: Authority) -> dict[str, Any]:
    return {
        "status": "V1.10-REJECTED / COMPLETE-FROZEN-RT14-SURFACE-REPAIRED",
        "rejectedCandidate": {
            "artifact": PREDECESSOR,
            "artifactSha256": PINS[PREDECESSOR],
            "checker": PREDECESSOR_CHECKER,
            "checkerSha256": PINS[PREDECESSOR_CHECKER],
            "independentReview": PREDECESSOR_REVIEW,
            "independentReviewSha256": PINS[PREDECESSOR_REVIEW],
            "reviewVerdict": "REJECT",
            "blockingFinding": REJECTION_ID,
        },
        "retainedFindingBoundary": (
            "The v1.10 review independently found its taxonomy, derivation, "
            "reducer equivalence, generic scope and hash-before-execution repairs "
            "sound. This successor retains those bytes exactly while accepting "
            "the review's sole compatibility blocker."
        ),
        "consumerAuthority": {
            "artifact": RT14,
            "artifactSha256": PINS[RT14],
            "checker": RT14_CHECKER,
            "checkerSha256": PINS[RT14_CHECKER],
            "independentReview": RT14_REVIEW,
            "independentReviewSha256": PINS[RT14_REVIEW],
        },
        "consumerSurface": _consumer_surface(authority),
        "authenticatedRestoration": {
            "V17": {
                "artifact": V17_DATA,
                "artifactSha256": PINS[V17_DATA],
                "checker": V17_CHECKER,
                "checkerSha256": PINS[V17_CHECKER],
                "runtimeKind": "module",
            },
            "V17.V16": {
                "artifact": V16_DATA,
                "artifactSha256": PINS[V16_DATA],
                "checker": V16_CHECKER,
                "checkerSha256": PINS[V16_CHECKER],
                "runtimeKind": "module",
            },
            "loadRule": (
                "V17 is the real module handle produced by executing pinned "
                "check-d9-v1.7.py bytes inside the authenticated v1.8 chain; its "
                "V16 is likewise produced from pinned check-d9.py bytes. No "
                "unverified filesystem-path import may supply either module."
            ),
            "publicCheckAdapter": (
                "check(candidate, predecessor, v16) first requires predecessor "
                "and v16 to equal the pinned v1.7/v1.6 data snapshots, then calls "
                "the authenticated v1.8 checker. v1.11 artifact validation remains "
                "private to the CLI and is not an overload of this public API."
            ),
        },
        "repairBoundary": (
            "Only complete consumer-surface metadata, the exact public three-"
            "argument check adapter, and authenticated V17 publication are added. "
            "No class, code, exit, axis, union, map, reducer, precedence, golden, "
            "identity, generic scope, remedy, or v1.10 reviewed semantic changes "
            "are permitted."
        ),
        "disposableProofBoundary": (
            "Selftest copies frozen RT14, updates the copied checker's D9 filename "
            "and hash pin plus the copied candidate's corresponding two authority "
            "fields, and retains the v1.8 D9 artifact. It then requires the copied "
            "RT14 checker normal run and mutation suite to pass. This is a checker-"
            "API compatibility probe, not a complete RT15 rebind and not acceptance "
            "or application of the rejected v1.8 authority."
        ),
        "authorityBoundary": (
            "CANDIDATE-NOT-APPLIED / NO RT15, E8, OP6, claim, TM, narrative, "
            "product, integration, application or seal authority"
        ),
    }


def _insert_after(root: dict[str, Any], after: str,
                  additions: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in root.items():
        result[key] = value
        if key == after:
            for added_key, added_value in additions:
                result[added_key] = added_value
    return result


PEER_REVIEW = (
    "A reviewer who authored neither v1.11 nor the D9/RT14 candidate lineage "
    "must verify stable input hashes, exact v1.11-to-v1.10 projection, the "
    "v1.10 REJECT binding, independent AST enumeration of every frozen RT14 "
    "D9 access and arity, authenticated V17/V16 module provenance, exact public "
    "three-argument check behavior, retained predecessor suites, hostile "
    "environment isolation, and the disposable RT14 checker-API compatibility "
    "normal plus selftest before application."
)
KNOWN_RESIDUAL = (
    "The v1.10 candidate remains rejected and is retained only as semantic and "
    "trust-boundary lineage. v1.11 is not independently reviewed or applied; no "
    "RT15 exists, and E8, RT14 and OP6 remain unrejoined. The disposable RT14 "
    "rebind is architecture test-double evidence, not implementation, product, "
    "integration, application or seal authority."
)


def _expected_successor(predecessor: dict[str, Any],
                        authority: Authority) -> dict[str, Any]:
    expected = copy.deepcopy(predecessor)
    expected["version"] = EXPECTED_VERSION
    expected["status"] = EXPECTED_STATUS
    expected["supersedes"] = PREDECESSOR
    expected["purpose"] = EXPECTED_PURPOSE
    expected["checkerTrustOrderContract"] = _trust_contract()
    expected = _insert_after(expected, "v19CompatibilityDisposition", [
        (COMPATIBILITY_KEY, _compatibility_disposition(authority)),
    ])
    expected["referenceDerivation"]["implementation"] = \
        REFERENCE_IMPLEMENTATION
    expected["conformanceClaims"] = [{
        "claim": EXPECTED_CLAIM,
        "reproduce": REPRODUCE,
        "mutationProof": MUTATION_PROOF,
    }]
    expected["peerReviewRequired"][-1] = PEER_REVIEW
    expected["knownLimitations"][-1] = KNOWN_RESIDUAL
    return expected


def _project_v110(candidate: dict[str, Any],
                  predecessor: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(candidate)
    projected.pop(COMPATIBILITY_KEY)
    for key in ("version", "status", "supersedes", "purpose"):
        projected[key] = copy.deepcopy(predecessor[key])
    for key in ("checkerTrustOrderContract", "referenceDerivation",
                "conformanceClaims", "peerReviewRequired", "knownLimitations"):
        projected[key] = copy.deepcopy(predecessor[key])
    return projected


def _first_difference(actual: Any, expected: Any,
                      path: str = "$") -> str | None:
    if type(actual) is not type(expected):
        return f"{path}: type {type(actual).__name__} != {type(expected).__name__}"
    if isinstance(actual, dict):
        if list(actual) != list(expected):
            return f"{path}: ordered keys {list(actual)!r} != {list(expected)!r}"
        for key in expected:
            difference = _first_difference(actual[key], expected[key], f"{path}.{key}")
            if difference:
                return difference
        return None
    if isinstance(actual, list):
        if len(actual) != len(expected):
            return f"{path}: length {len(actual)} != {len(expected)}"
        for index, (left, right) in enumerate(zip(actual, expected)):
            difference = _first_difference(left, right, f"{path}[{index}]")
            if difference:
                return difference
        return None
    if actual != expected:
        return f"{path}: {actual!r} != {expected!r}"
    return None


def _resolve_path(module: Any, path: str) -> Any:
    value = module
    for part in path.split("."):
        value = getattr(value, part)
    return value


def _positional_arity(value: Any) -> int | None:
    try:
        parameters = list(inspect.signature(value).parameters.values())
    except (TypeError, ValueError):
        return None
    if any(parameter.kind in (parameter.VAR_POSITIONAL,
                              parameter.VAR_KEYWORD)
           for parameter in parameters):
        return None
    return len([
        parameter for parameter in parameters
        if parameter.kind in (parameter.POSITIONAL_ONLY,
                              parameter.POSITIONAL_OR_KEYWORD)
    ])


def _surface_resolution_findings(module: Any,
                                 surface: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    for declaration in surface.get("requiredTopLevelExports", []):
        name = declaration.get("name") if isinstance(declaration, dict) else None
        try:
            value = getattr(module, name)
        except (AttributeError, TypeError):
            findings.append(f"D30-RUNTIME-SURFACE: missing top-level {name!r}")
            continue
        if declaration.get("kind") == "module" and \
                not isinstance(value, types.ModuleType):
            findings.append(f"D30-RUNTIME-SURFACE: {name} is not a module")
        if declaration.get("kind") == "callable":
            if not callable(value):
                findings.append(f"D30-RUNTIME-SURFACE: {name} is not callable")
            elif _positional_arity(value) != declaration.get("positionalArity"):
                findings.append(f"D30-RUNTIME-SURFACE: {name} arity drifted")
    for declaration in surface.get("requiredChainedExports", []):
        path = declaration.get("path") if isinstance(declaration, dict) else "?"
        try:
            value = _resolve_path(module, path)
        except (AttributeError, TypeError):
            findings.append(f"D30-RUNTIME-SURFACE: missing chain {path}")
            continue
        if declaration.get("kind") == "module" and \
                not isinstance(value, types.ModuleType):
            findings.append(f"D30-RUNTIME-SURFACE: {path} is not a module")
        if declaration.get("kind") == "callable":
            if not callable(value):
                findings.append(f"D30-RUNTIME-SURFACE: {path} is not callable")
            elif _positional_arity(value) != declaration.get("positionalArity"):
                findings.append(f"D30-RUNTIME-SURFACE: {path} arity drifted")
    return findings


def _runtime_invocation_findings(module: types.ModuleType,
                                 authority: Authority) -> list[str]:
    findings: list[str] = []
    try:
        admitted = authority.rt14["contextualD9Rejoin"]["contextSplit"][
            "admittedAuthorizedCustodyLoss"]
        axes = copy.deepcopy(admitted["coreCompletionMatrix"][0]["axes"])
        maps = authority.v18["codeMaps"]
        precedence = authority.v18["causeModel"]["precedence"]
        control = authority.rt14["contextualD9Rejoin"]["faultPrecedenceControl"]
        if module.derive_class(copy.deepcopy(axes)) != \
                authority.v18_checker.derive_class(copy.deepcopy(axes)):
            findings.append("D30-RUNTIME-INVOKE: derive_class drifted")
        if module.derive_codes(copy.deepcopy(axes), maps) != \
                authority.v18_checker.derive_codes(copy.deepcopy(axes), maps):
            findings.append("D30-RUNTIME-INVOKE: derive_codes drifted")
        if module.reduce_concurrent(
                copy.deepcopy(control["conditions"]), list(precedence)) != \
                authority.v18_checker.reduce_concurrent(
                    copy.deepcopy(control["conditions"]), list(precedence)):
            findings.append("D30-RUNTIME-INVOKE: reduce_concurrent drifted")
        if module.V17 is not authority.v17_checker or \
                module.V17.V16 is not authority.v16_checker:
            findings.append("D30-RUNTIME-INVOKE: V17/V16 is not authenticated chain")
        if module.V17.V16.derive_class(copy.deepcopy(axes)) != \
                authority.v16_checker.derive_class(copy.deepcopy(axes)):
            findings.append("D30-RUNTIME-INVOKE: chained derive_class drifted")
        retained = module.check(
            copy.deepcopy(authority.v18), copy.deepcopy(authority.v17),
            copy.deepcopy(authority.v16))
        if retained:
            findings.append(
                f"D30-RUNTIME-INVOKE: three-argument check returned {retained[0]}")
        wrong = module.check(
            copy.deepcopy(authority.v18), {}, copy.deepcopy(authority.v16))
        if wrong != [
                "D30-COMPAT-AUTHORITY: predecessor is not pinned v1.7 data"]:
            findings.append("D30-RUNTIME-INVOKE: wrong v1.7 authority was not rejected")
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        findings.append(
            f"D30-RUNTIME-INVOKE: controlled invocation raised {type(exc).__name__}")
    return findings


def _public_api_view() -> types.ModuleType:
    """Return the exact exports without relying on sys.modules registration."""
    module = types.ModuleType("opensip_d9_v111_public_api_view")
    module.check = check
    module.derive_class = derive_class
    module.derive_codes = derive_codes
    module.reduce_concurrent = reduce_concurrent
    module.V17 = V17
    return module


def _check_contract(candidate: object, authority: Authority) -> list[str]:
    if not isinstance(candidate, dict) or not candidate:
        return ["D9-TOTALITY-ROOT: v1.11 candidate must be a nonempty object"]
    findings: list[str] = []
    try:
        expected = _expected_successor(authority.predecessor, authority)
        try:
            projected = _project_v110(candidate, authority.predecessor)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
            findings.append(
                f"D31-PROJECTION: cannot project v1.11 to v1.10 "
                f"({type(exc).__name__})")
            projected = None
        if projected is not None:
            difference = _first_difference(projected, authority.predecessor)
            if difference:
                findings.append(
                    "D31-PROJECTION: v1.11 does not project exactly to pinned "
                    f"v1.10; first difference: {difference}")
            retained = authority.v110_checker.check(
                projected, authority.v110_authority)
            findings.extend(f"D0..D29 retained checker: {item}" for item in retained)

        actual_calls = _enumerate_rt14_calls(authority.snapshots[RT14_CHECKER])
        if actual_calls != EXPECTED_CALL_SITES:
            findings.append(
                "D30-AST-SURFACE: pinned RT14 call surface differs from exact "
                "six-site authority")
        disposition = candidate.get(COMPATIBILITY_KEY)
        declared_surface = disposition.get("consumerSurface") \
            if isinstance(disposition, dict) else None
        if declared_surface != _consumer_surface(authority):
            findings.append("D30-AST-SURFACE: candidate declaration is not recomputed")
        public_api = _public_api_view()
        if isinstance(declared_surface, dict):
            findings.extend(_surface_resolution_findings(
                public_api, declared_surface))
        findings.extend(_runtime_invocation_findings(public_api, authority))

        for key in ("classToExitCode", "hostTerminationUnion",
                    "scenarioAxesSchema", "codeMaps", "causeModel",
                    "goldenCases", "hostDerivedUnsatisfiableFinalizationContract"):
            if candidate.get(key) != authority.predecessor.get(key):
                findings.append(f"D31-NONEXPANSION: {key} changed")
        difference = _first_difference(candidate, expected)
        if difference:
            findings.append(
                "D32-EXACT-DELTA: candidate differs outside the closed v1.11 "
                f"successor; first difference: {difference}")
    except (AttributeError, IndexError, KeyError, StopIteration, TypeError,
            ValueError) as exc:
        findings.append(
            f"D9-TOTALITY-EXCEPTION: malformed parsed shape "
            f"({type(exc).__name__})")
    return findings


def _disposition(root: dict[str, Any]) -> dict[str, Any]:
    value = root[COMPATIBILITY_KEY]
    if not isinstance(value, dict):
        raise TypeError(COMPATIBILITY_KEY)
    return value


def _surface(root: dict[str, Any]) -> dict[str, Any]:
    value = _disposition(root)["consumerSurface"]
    if not isinstance(value, dict):
        raise TypeError("consumerSurface")
    return value


def _named(rows: list[dict[str, Any]], name: str) -> dict[str, Any]:
    return next(row for row in rows if row.get("name") == name)


def _remove_named(rows: list[dict[str, Any]], name: str) -> None:
    rows.remove(_named(rows, name))


Mutation = tuple[str, Callable[[dict[str, Any]], None]]
MUTATIONS: list[Mutation] = [
    ("version", lambda root: root.__setitem__("version", "v1.10")),
    ("status promotion", lambda root: root.__setitem__("status", "APPLIED")),
    ("wrong supersedes", lambda root: root.__setitem__("supersedes", V19)),
    ("drop v1.10 disposition", lambda root: root.pop(COMPATIBILITY_KEY)),
    ("accept v1.10", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("reviewVerdict", "PASS")),
    ("wrong v1.10 artifact pin", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("artifactSha256", "0" * 64)),
    ("wrong v1.10 checker pin", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("checkerSha256", "0" * 64)),
    ("wrong v1.10 review pin", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("independentReviewSha256", "0" * 64)),
    ("wrong blocking finding", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("blockingFinding", "NONE")),
    ("incomplete call enumeration", lambda root: _surface(root)["callSites"].pop()),
    ("fabricated call enumeration", lambda root: _surface(root)["callSites"].append({"line": 999, "path": "other", "positionalArity": 0, "keywordNames": []})),
    ("drop V17 declaration", lambda root: _remove_named(_surface(root)["requiredTopLevelExports"], "V17")),
    ("wrong V17 kind", lambda root: _named(_surface(root)["requiredTopLevelExports"], "V17").__setitem__("kind", "callable")),
    ("drop check declaration", lambda root: _remove_named(_surface(root)["requiredTopLevelExports"], "check")),
    ("wrong check arity", lambda root: _named(_surface(root)["requiredTopLevelExports"], "check").__setitem__("positionalArity", 2)),
    ("extra consumer export", lambda root: _surface(root)["requiredTopLevelExports"].append({"name": "trusted", "kind": "callable", "positionalArity": 0})),
    ("drop V16 chain", lambda root: _surface(root)["requiredChainedExports"].pop(0)),
    ("wrong chained derive", lambda root: _surface(root)["requiredChainedExports"][1].__setitem__("path", "V17.derive_class")),
    ("claim wrapper V17", lambda root: _disposition(root)["authenticatedRestoration"]["V17"].__setitem__("runtimeKind", "wrapper")),
    ("unverified V17 load", lambda root: _disposition(root)["authenticatedRestoration"].__setitem__("loadRule", "import by path")),
    ("overload public check", lambda root: _disposition(root)["authenticatedRestoration"].__setitem__("publicCheckAdapter", "check(*args)")),
    ("broaden repair", lambda root: _disposition(root).__setitem__("repairBoundary", "change taxonomy")),
    ("claim RT15", lambda root: _disposition(root).__setitem__("authorityBoundary", "RT15 APPLIED")),
    ("drop trust contract", lambda root: root.pop("checkerTrustOrderContract")),
    ("change v1.10 pin", lambda root: root["checkerTrustOrderContract"]["transitiveInputs"][0].__setitem__("sha256", "0" * 64)),
    ("drop inherited pin", lambda root: root["checkerTrustOrderContract"]["transitiveInputs"].pop()),
    ("execute before verify", lambda root: root["checkerTrustOrderContract"]["requiredOrder"].reverse()),
    ("old reference", lambda root: root["referenceDerivation"].__setitem__("implementation", "artifacts/check-d9-v1.10.py")),
    ("weaken conformance", lambda root: root["conformanceClaims"][0].__setitem__("claim", "exports listed")),
    ("drop independent review", lambda root: root["peerReviewRequired"].pop()),
    ("drop residual", lambda root: root["knownLimitations"].pop()),
    ("change exit", lambda root: root["classToExitCode"].__setitem__("request-rejected", 4)),
]


def _trust_order_probes(loader: DeferredAuthorityLoader
                        ) -> list[tuple[str, bool]]:
    probes: list[tuple[str, bool]] = []
    for corrupt_name in PINS:
        invoked = 0

        def reader(path: pathlib.Path, target: str = corrupt_name) -> bytes:
            source = path.read_bytes()
            return source + b"\n# trust-order mutation\n" \
                if path.name == target else source

        def marker(_snapshots: Mapping[str, bytes],
                   _parsed: Mapping[str, Any]) -> None:
            nonlocal invoked
            invoked += 1

        rejected = False
        try:
            loader.invoke_verified(marker, reader)
        except AuthorityLoadError:
            rejected = True
        probes.append((
            f"pin mismatch blocks callback: {corrupt_name}",
            rejected and invoked == 0,
        ))
    clean_invoked = 0

    def clean_marker(_snapshots: Mapping[str, bytes],
                     _parsed: Mapping[str, Any]) -> str:
        nonlocal clean_invoked
        clean_invoked += 1
        return "after-verification"

    try:
        _, _, result = loader.invoke_verified(clean_marker)
        clean = clean_invoked == 1 and result == "after-verification"
    except AuthorityLoadError:
        clean = False
    probes.append(("clean callback invoked exactly once after verification", clean))
    return probes


def _write_pyc(path: pathlib.Path, marker: pathlib.Path) -> None:
    code = compile(
        f"from pathlib import Path\nPath({str(marker)!r}).write_text('PYC')\n",
        str(path), "exec")
    header = importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, 0, 0)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(header + marshal.dumps(code))


def _environment_probes(loader: DeferredAuthorityLoader
                        ) -> list[tuple[str, bool]]:
    probes: list[tuple[str, bool]] = []
    module_name = "opensip_check_d9_v110_verified"
    prior = sys.modules.get(module_name)
    hostile = types.ModuleType(module_name)
    hostile.V17 = object()
    sys.modules[module_name] = hostile
    try:
        _, _, loaded = loader.invoke_verified(_execute_verified_v110)
        passed = isinstance(loaded, tuple) and loaded[0] is not hostile
    except AuthorityLoadError:
        passed = False
    finally:
        if prior is None:
            sys.modules.pop(module_name, None)
        else:
            sys.modules[module_name] = prior
    probes.append(("hostile sys.modules entry ignored", passed))

    trusted = {name: (HERE / name).read_bytes() for name in PINS}
    with tempfile.TemporaryDirectory(prefix="opensip-d9-v111-env-") as raw:
        directory = pathlib.Path(raw)
        for name, source in trusted.items():
            (directory / name).write_bytes(source)
        marker = directory / "path-marker"
        malicious = trusted[PREDECESSOR_CHECKER] + (
            f"\npathlib.Path({str(marker)!r}).write_text('PATH')\n".encode())
        (directory / PREDECESSOR_CHECKER).write_bytes(malicious)
        try:
            _execute_snapshot("d9_v110_malicious_control",
                              PREDECESSOR_CHECKER, malicious)
            control_fired = marker.exists()
        except Exception:
            control_fired = False
        marker.unlink(missing_ok=True)

        def trusted_reader(path: pathlib.Path) -> bytes:
            return trusted[path.name]

        try:
            DeferredAuthorityLoader(directory).invoke_verified(
                _execute_verified_v110, trusted_reader)
            isolated = not marker.exists()
        except AuthorityLoadError:
            isolated = False
        probes.append(("verified snapshot defeats disk path swap",
                       control_fired and isolated))

        (directory / PREDECESSOR_CHECKER).write_bytes(
            trusted[PREDECESSOR_CHECKER])
        pyc_marker = directory / "pyc-marker"
        tag = sys.implementation.cache_tag or "python"
        pyc = directory / "__pycache__" / f"check-d9-v1.10.{tag}.pyc"
        _write_pyc(pyc, pyc_marker)
        try:
            importlib.machinery.SourcelessFileLoader(
                "d9_v110_malicious_pyc_control", str(pyc)).load_module()
            pyc_control = pyc_marker.exists()
        except Exception:
            pyc_control = False
        pyc_marker.unlink(missing_ok=True)
        try:
            DeferredAuthorityLoader(directory).load()
            pyc_isolated = not pyc_marker.exists()
        except AuthorityLoadError:
            pyc_isolated = False
        probes.append(("malicious pyc ignored", pyc_control and pyc_isolated))
    return probes


def _ast_probes(authority: Authority) -> list[tuple[str, bool]]:
    source = authority.snapshots[RT14_CHECKER]
    actual = _enumerate_rt14_calls(source)
    added = source + b"\n# AST probe\ndef _probe(d9mod):\n    d9mod.other()\n"
    shortened = source.replace(
        b"d9mod.V17.V16.derive_class(first_axes)",
        b"d9mod.V17.derive_class(first_axes)", 1)
    return [
        ("exact six frozen call sites derived", actual == EXPECTED_CALL_SITES),
        ("loader check arity is three", any(
            row["path"] == "check" and row["positionalArity"] == 3
            for row in actual)),
        ("direct derive_class has two sites", len([
            row for row in actual if row["path"] == "derive_class"]) == 2),
        ("full V17.V16 chain retained", any(
            row["path"] == "V17.V16.derive_class" for row in actual)),
        ("added consumer access changes enumeration",
         _enumerate_rt14_calls(added) != actual),
        ("shortened chain changes enumeration",
         _enumerate_rt14_calls(shortened) != actual),
    ]


def _runtime_mutation_probes(authority: Authority) -> list[tuple[str, bool]]:
    surface = _consumer_surface(authority)

    def base_module() -> types.ModuleType:
        module = types.ModuleType("d9_v111_surface_probe")
        module.check = check
        module.derive_class = derive_class
        module.derive_codes = derive_codes
        module.reduce_concurrent = reduce_concurrent
        module.V17 = V17
        return module

    variants: list[tuple[str, Callable[[types.ModuleType], None]]] = [
        ("missing V17", lambda module: delattr(module, "V17")),
        ("V17 is not module", lambda module: setattr(module, "V17", object())),
        ("missing V16 chain", lambda module: setattr(
            module, "V17", types.ModuleType("v17_without_v16"))),
        ("chained derive noncallable", lambda module: setattr(
            module.V17.V16, "derive_class", None)),
        ("check wrong arity", lambda module: setattr(
            module, "check", lambda candidate, predecessor: [])),
    ]
    probes: list[tuple[str, bool]] = []
    for name, mutate in variants:
        module = base_module()
        if name == "chained derive noncallable":
            copied_v17 = types.ModuleType("copied_v17")
            copied_v16 = types.ModuleType("copied_v16")
            copied_v16.derive_class = authority.v16_checker.derive_class
            copied_v17.V16 = copied_v16
            module.V17 = copied_v17
        mutate(module)
        probes.append((name, bool(_surface_resolution_findings(module, surface))))
    return probes


def _rt14_rebind_probe() -> tuple[bool, str]:
    """Run an honest disposable RT14 checker-API compatibility probe."""
    checker_digest = hashlib.sha256((HERE / CHECKER).read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix="opensip-d9-v111-rt14-") as raw:
        directory = pathlib.Path(raw) / "artifacts"
        directory.mkdir()
        for source in HERE.iterdir():
            if source.is_file():
                shutil.copy2(source, directory / source.name)

        frozen_source = (directory / RT14_CHECKER).read_text()
        name_line = 'D9_CHECKER = "check-d9-v1.8.py"'
        replacement_line = f'D9_CHECKER = "{CHECKER}"'
        old_digest = PINS[V18_CHECKER]
        if frozen_source.count(name_line) != 1 or \
                frozen_source.count(old_digest) != 1:
            return False, "frozen RT14 checker replacement anchors drifted"
        rebound_source = frozen_source.replace(name_line, replacement_line, 1)
        rebound_source = rebound_source.replace(old_digest, checker_digest, 1)
        rebound_checker = directory / "check-retention-custody-v14-d9-v111-sim.py"
        rebound_checker.write_text(rebound_source)

        candidate = json.loads((directory / RT14).read_text())
        authority_row = candidate["contextualD9Rejoin"]["authority"]
        authority_row["d9Checker"] = CHECKER
        authority_row["d9CheckerSha256"] = checker_digest
        rebound_candidate = directory / "retention-tiers.v14-d9-v111-sim.json"
        rebound_candidate.write_text(json.dumps(candidate, indent=2) + "\n")

        outputs: list[str] = []
        for extra in ([], ["--selftest"]):
            command = [
                sys.executable, "-B", str(rebound_checker),
                str(rebound_candidate), *extra,
            ]
            completed = subprocess.run(
                command, cwd=directory, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, timeout=180, check=False)
            outputs.append(completed.stdout)
            if completed.returncode != 0:
                tail = "\n".join(completed.stdout.splitlines()[-20:])
                return False, f"{'selftest' if extra else 'normal'} failed:\n{tail}"
        return True, "RT14 normal and selftest passed"


HOSTILE_ROOTS: list[tuple[str, Any]] = [
    ("null", None), ("false", False), ("zero", 0), ("string", "hostile"),
    ("array", []), ("empty object", {}), ("float", 1.5), ("bytes", b"x"),
]


def _hostile_candidates(candidate: dict[str, Any]) -> list[tuple[str, Any]]:
    cases = list(HOSTILE_ROOTS)
    for key in (
            "rejectedPredecessor", "checkerTrustOrderContract",
            "v19CompatibilityDisposition", COMPATIBILITY_KEY, "exitClasses",
            "referenceDerivation", "conformanceClaims", "invariants",
            "goldenCases", "peerReviewRequired", "knownLimitations",
            "crossAxisInvariants", "scenarioAxesSchema", "classToExitCode",
            "hostTerminationUnion", "codeMaps", "causeModel",
            "hostDerivedUnsatisfiableFinalizationContract"):
        for value in (None, "hostile"):
            changed = copy.deepcopy(candidate)
            changed[key] = value
            cases.append((f"{key}={type(value).__name__}", changed))
    return cases


def selftest(candidate: dict[str, Any], authority: Authority,
             loader: DeferredAuthorityLoader) -> int:
    base_findings = _check_contract(candidate, authority)
    if base_findings:
        print(f"REFUSING to self-test: base has {len(base_findings)} finding(s)")
        for finding in base_findings[:12]:
            print("  -", finding)
        return 1

    projected = _project_v110(candidate, authority.predecessor)
    print("retained v1.10/v1.9/v1.8/v1.7/v1.6 mutation proof")
    if authority.v110_checker.selftest(
            projected, authority.v110_authority,
            authority.v110_checker.DeferredAuthorityLoader()) != 0:
        return 1

    print("\nv1.11 closed-successor mutations — every row must be REJECTED\n")
    escaped = 0
    for name, mutate in MUTATIONS:
        changed = copy.deepcopy(candidate)
        before = copy.deepcopy(changed)
        try:
            mutate(changed)
            if changed == before:
                raise ValueError("mutation did not change candidate")
            findings = _check_contract(changed, authority)
        except Exception as exc:
            findings = []
            print(f"  ESCAPE  {name}\n          harness raised {type(exc).__name__}")
            escaped += 1
            continue
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")
        print(f"          {findings[0] if findings else 'NO FINDING'}")

    sections: list[tuple[str, list[tuple[str, bool]]]] = [
        ("trust-order", _trust_order_probes(loader)),
        ("AST consumer-surface", _ast_probes(authority)),
        ("runtime surface mutations", _runtime_mutation_probes(authority)),
        ("malicious environment", _environment_probes(loader)),
    ]
    probe_failures = 0
    probe_count = 0
    for label, probes in sections:
        print(f"\nv1.11 {label} probes — every row must PASS\n")
        for name, passed in probes:
            probe_count += 1
            probe_failures += 0 if passed else 1
            print(f"  {'pass' if passed else 'FAIL':>6}  {name}")

    print("\nv1.11 hostile parsed shapes — every row must be REJECTED\n")
    hostile_failures = 0
    hostile = _hostile_candidates(candidate)
    for name, value in hostile:
        try:
            findings = _check_contract(value, authority)
        except Exception as exc:
            findings = []
            print(f"    FAIL  {name}: raised {type(exc).__name__}")
        if not findings:
            hostile_failures += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")

    print("\ndisposable frozen-RT14 checker-API compatibility probe\n")
    rebind_passed, rebind_detail = _rt14_rebind_probe()
    print(f"  {'pass' if rebind_passed else 'FAIL':>6}  {rebind_detail}")

    print()
    if escaped or probe_failures or hostile_failures or not rebind_passed:
        print(
            f"v1.11 failures: {escaped}/{len(MUTATIONS)} artifact mutations "
            f"escaped; {probe_failures}/{probe_count} probes failed; "
            f"{hostile_failures}/{len(hostile)} hostile shapes escaped; "
            f"RT14 API probe={'pass' if rebind_passed else 'FAIL'}")
        return 1
    print(
        f"all {len(MUTATIONS)} v1.11 artifact mutations rejected; "
        f"{probe_count} trust/AST/runtime/environment probes passed; "
        f"{len(hostile)} hostile shapes rejected; retained predecessor suites "
        "passed; disposable RT14 checker-API normal+selftest passed")
    return 0


def main() -> int:
    positional = [argument for argument in sys.argv[1:]
                  if argument != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        candidate = load(path)
    except (OSError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError) as exc:
        print(f"cannot load D9 candidate: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2

    authority = _BOOTSTRAP_AUTHORITY
    loader = DeferredAuthorityLoader()
    if "--selftest" in sys.argv[1:]:
        if not isinstance(candidate, dict):
            print("selftest requires an object root", file=sys.stderr)
            return 1
        return selftest(candidate, authority, loader)

    findings = _check_contract(candidate, authority)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    print(
        f"D9 v1.11 contract OK — {path.name}, 6 frozen RT14 call sites, "
        f"{len(TOP_LEVEL_EXPORTS)} top-level and {len(CHAINED_EXPORTS)} chained "
        f"exports resolved, {len(PINS)} pins verified before import, exact "
        "v1.10 projection, retained D0..D29 clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
