#!/usr/bin/env python3
"""Canonical raw-representation successor checker for D9 v1.12.

v1.12 preserves rejected v1.11's complete frozen-RT14 public API and parsed
semantics, while repairing the raw JSON representation defect found by the
independent v1.11 review.  The exact candidate bytes must equal one deterministic
``json.dumps(..., indent=2, ensure_ascii=True, sort_keys=False) + "\\n"``
serialization of the mechanically constructed ordered successor object.

All predecessor, checker, review and consumer bytes are hash-verified before
retained source snapshots execute.  Public ``check`` remains RT14's exact v1.8
three-argument compatibility API; v1.12 validation remains private.

Authorship disclosure: this checker author also authored the v1.11 independent
rejection review and therefore cannot independently approve v1.12.

Usage: python3 -B artifacts/check-d9-v1.12.py [contract] [--selftest]
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
BINDING = "d9-exit-contract.v1.12.json"
CHECKER = "check-d9-v1.12.py"
PREDECESSOR = "d9-exit-contract.v1.11.json"
PREDECESSOR_CHECKER = "check-d9-v1.11.py"
PREDECESSOR_REVIEW = \
    "d9-exit-contract.v1.11.review-independent-prefreeze.json"
V110 = "d9-exit-contract.v1.10.json"
V110_CHECKER = "check-d9-v1.10.py"
V110_REVIEW = "d9-exit-contract.v1.10.review-independent-prefreeze.json"
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

EXPECTED_VERSION = "v1.12"
EXPECTED_STATUS = (
    "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW "
    "(v1.12 canonical raw-preservation repair over rejected v1.11)"
)
EXPECTED_PURPOSE = (
    "Total host-owned process-exit contract: preserve v1.11 complete frozen-RT14 "
    "public API and parsed semantics while restoring and mechanically enforcing "
    "one deterministic canonical raw JSON representation for the inherited "
    "protected projection."
)
REFERENCE_IMPLEMENTATION = (
    "artifacts/check-d9-v1.12.py::"
    "check+derive_class+derive_codes+reduce_concurrent+V17.V16.derive_class"
)
REPRODUCE = (
    "python3 -B artifacts/check-d9-v1.12.py         # defaults to the binding "
    "v1.12 artifact"
)
MUTATION_PROOF = (
    "python3 -B artifacts/check-d9-v1.12.py --selftest  # raw-equivalent "
    "mutations, all pins, hostile environments, complete RT14 surface, "
    "retained predecessor suites and disposable RT14 API normal+selftest"
)
EXPECTED_CLAIM = (
    "The exact ordered v1.12 object projects to rejected v1.11; its protected "
    "inherited raw spans project byte-for-byte to pinned v1.10 under the declared "
    "canonical representation; and the complete frozen RT14 API remains "
    "authenticated and behaviorally unchanged."
)
COMPATIBILITY_KEY = "v111RepresentationDisposition"
REJECTION_ID = "D9V111-PF-01-INHERITED-RAW-BYTE-DRIFT"
V110_COMPATIBILITY_KEY = "v110CompatibilityDisposition"

V110_RETAINED_BOUNDARY = (
    "The v1.10 review independently found its taxonomy, derivation, reducer "
    "equivalence, generic scope and hash-before-execution repairs sound. v1.11 "
    "preserved those parsed semantics while repairing the complete frozen RT14 "
    "runtime surface; v1.12 preserves the same parsed semantics and proves the "
    "canonical raw protected projection against pinned v1.10. This accepts "
    "neither rejected predecessor."
)

INHERITED_PINS: dict[str, str] = {
    V110: "bf1d7eb0ab24de89f665f46c25377195a2721fc7fcb62f3aa449d0887b705b7b",
    V110_CHECKER: "77f86334a0ee016960224880fe75ef2b9b44d3adf20799c8354e992fbf19cca6",
    V110_REVIEW: "7faefdf8f2c19e39ad9fdd6fba8df6f08c586aa73b7e5ab7ed917ae4c223e476",
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
    PREDECESSOR: "09ab6b579173bdbd9575d46e7df96b8279a0bb12512638e25ad56e28d16e9895",
    PREDECESSOR_CHECKER: "9b637adee48432bb5388ce51212d59a1965044d2c1d5f6b6a4a3dd8ed519000a",
    PREDECESSOR_REVIEW: "df1e89324a6c7645e96f69a2cc924731e4e37eeea64c10058cdd4cfcdfdbbcec",
    **INHERITED_PINS,
}
ROLES = {
    PREDECESSOR: "rejected v1.11 candidate projected at the ordered-object boundary",
    PREDECESSOR_CHECKER: "retained executable v1.11 public API and semantic checker",
    PREDECESSOR_REVIEW: "independent v1.11 REJECT and representation-repair authority",
    V110: "rejected v1.10 data supplying the protected raw projection",
    V110_CHECKER: "retained executable v1.10 checker",
    V110_REVIEW: "independent v1.10 rejection authority",
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

PROTECTED_RAW_ROOTS = [
    "exitClasses", "classToExitCode", "codeVocabulary",
    "scenarioAxesSchema", "hostTerminationUnion", "codeMaps", "causeModel",
    "crossAxisInvariants", "concurrentConditionReducer",
    "concurrentConditionGoldens", "goldenCases",
    "hostDerivedUnsatisfiableFinalizationContract", "finalizationTransitions",
    "nonAnalysisDerivation", "resolves", "invariants",
]
PROTECTED_ARRAY_PREFIXES = {
    "peerReviewRequired": [0, 1, 2],
    "knownLimitations": [0, 1, 2, 3, 4],
}
LEXICAL_LEAVES = [
    ("$.codeVocabulary.spellingMigration.note", "codeVocabulary"),
    ("$.crossAxisInvariants[8].why", "crossAxisInvariants"),
    ("$.hostTerminationUnion.forbiddenFieldsRationale", "hostTerminationUnion"),
    ("$.invariants[0].text", "invariants"),
    ("$.knownLimitations[4]", "knownLimitations[4]"),
    ("$.peerReviewRequired[0]", "peerReviewRequired[0]"),
    ("$.resolves.A1-D9-V15-01", "resolves"),
    ("$.resolves.A1-D9-V15-02", "resolves"),
    ("$.resolves.A1-D9-V15-04", "resolves"),
    ("$.resolves.A1-D9-V15-05", "resolves"),
    ("$.resolves.A1-D9-V15-06", "resolves"),
    ("$.resolves.B-D9V15-01", "resolves"),
    ("$.resolves.B-D9V15-02", "resolves"),
    ("$.resolves.B-D9V15-03", "resolves"),
    ("$.resolves.B-D9V15-04", "resolves"),
    ("$.resolves.B-D9V15-05", "resolves"),
    ("$.scenarioAxesSchema.properties.rejectionCause.why", "scenarioAxesSchema"),
]
LEXICAL_ACCESSORS: dict[str, tuple[object, ...]] = {
    "$.codeVocabulary.spellingMigration.note":
        ("codeVocabulary", "spellingMigration", "note"),
    "$.crossAxisInvariants[8].why": ("crossAxisInvariants", 8, "why"),
    "$.hostTerminationUnion.forbiddenFieldsRationale":
        ("hostTerminationUnion", "forbiddenFieldsRationale"),
    "$.invariants[0].text": ("invariants", 0, "text"),
    "$.knownLimitations[4]": ("knownLimitations", 4),
    "$.peerReviewRequired[0]": ("peerReviewRequired", 0),
    "$.resolves.A1-D9-V15-01": ("resolves", "A1-D9-V15-01"),
    "$.resolves.A1-D9-V15-02": ("resolves", "A1-D9-V15-02"),
    "$.resolves.A1-D9-V15-04": ("resolves", "A1-D9-V15-04"),
    "$.resolves.A1-D9-V15-05": ("resolves", "A1-D9-V15-05"),
    "$.resolves.A1-D9-V15-06": ("resolves", "A1-D9-V15-06"),
    "$.resolves.B-D9V15-01": ("resolves", "B-D9V15-01"),
    "$.resolves.B-D9V15-02": ("resolves", "B-D9V15-02"),
    "$.resolves.B-D9V15-03": ("resolves", "B-D9V15-03"),
    "$.resolves.B-D9V15-04": ("resolves", "B-D9V15-04"),
    "$.resolves.B-D9V15-05": ("resolves", "B-D9V15-05"),
    "$.scenarioAxesSchema.properties.rejectionCause.why":
        ("scenarioAxesSchema", "properties", "rejectionCause", "why"),
}


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


def load_source(path: pathlib.Path) -> tuple[Any, bytes]:
    source = path.read_bytes()
    return _parse_json_bytes(source, path.name), source


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


def _execute_verified_v111(
        snapshots: Mapping[str, bytes], _parsed: Mapping[str, Any]
) -> tuple[types.ModuleType, Any]:
    """Build v1.11 authority only after the whole outer closure is verified."""
    module = _execute_snapshot(
        "opensip_check_d9_v111_verified", PREDECESSOR_CHECKER,
        snapshots[PREDECESSOR_CHECKER])
    if dict(getattr(module, "PINS", {})) != INHERITED_PINS:
        raise AuthorityLoadError("v1.11 executable transitive pin set drifted")
    authority = getattr(module, "_BOOTSTRAP_AUTHORITY", None)
    inherited = getattr(authority, "snapshots", None)
    if not isinstance(inherited, Mapping) or any(
            inherited.get(name) != snapshots[name] for name in INHERITED_PINS):
        raise AuthorityLoadError(
            "executed v1.11 authority did not use the outer verified snapshots")
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
                 v110: dict[str, Any],
                 rt14: dict[str, Any], rt14_review: dict[str, Any],
                 v18: dict[str, Any], v17: dict[str, Any],
                 v16: dict[str, Any], v111_checker: types.ModuleType,
                 v111_authority: Any, v18_checker: types.ModuleType,
                 v17_checker: types.ModuleType,
                 v16_checker: types.ModuleType):
        self.snapshots = snapshots
        self.predecessor = predecessor
        self.predecessor_review = predecessor_review
        self.v110 = v110
        self.rt14 = rt14
        self.rt14_review = rt14_review
        self.v18 = v18
        self.v17 = v17
        self.v16 = v16
        self.v111_checker = v111_checker
        self.v111_authority = v111_authority
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
            raise AuthorityLoadError("pinned v1.11 review is not the exact REJECT")
        window = review.get("hashWindow") or {}
        expected_window = {
            PREDECESSOR: PINS[PREDECESSOR],
            PREDECESSOR_CHECKER: PINS[PREDECESSOR_CHECKER],
            **INHERITED_PINS,
        }
        if window.get("startEqualsEnd") is not True or \
                window.get("inputHashDrift") is not False or \
                window.get("start") != expected_window or \
                window.get("end") != expected_window:
            raise AuthorityLoadError("v1.11 review hash window does not bind all inputs")
        subjects = {
            row.get("path"): row.get("sha256")
            for row in (review.get("reviewBinding") or {}).get(
                "exactSubjects", []) if isinstance(row, dict)
        }
        if subjects != {
                PREDECESSOR: PINS[PREDECESSOR],
                PREDECESSOR_CHECKER: PINS[PREDECESSOR_CHECKER]}:
            raise AuthorityLoadError("v1.11 review exactSubjects drifted")
        blockers = [
            row.get("id") for row in review.get("blockingFindings", [])
            if isinstance(row, dict)
        ]
        if blockers != [REJECTION_ID]:
            raise AuthorityLoadError("v1.11 review blocker drifted")
        return parsed

    def invoke_verified(self, callback: ImportCallback,
                        byte_reader: ReadBytes | None = None
                        ) -> tuple[Mapping[str, bytes], Mapping[str, Any], Any]:
        snapshots = self._snapshots(byte_reader)
        parsed = self._parsed(snapshots)
        result = callback(snapshots, parsed)
        return snapshots, parsed, result

    def load(self) -> Authority:
        snapshots, parsed, loaded = self.invoke_verified(_execute_verified_v111)
        if not isinstance(loaded, tuple) or len(loaded) != 2 or \
                not isinstance(loaded[0], types.ModuleType):
            raise AuthorityLoadError("verified importer did not return v1.11 authority")
        v111_checker, v111_authority = loaded
        try:
            v18_checker = v111_authority.v18_checker
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
            v110=parsed[V110],
            rt14=parsed[RT14],
            rt14_review=parsed[RT14_REVIEW],
            v18=parsed[V18],
            v17=parsed[V17_DATA],
            v16=parsed[V16_DATA],
            v111_checker=v111_checker,
            v111_authority=v111_authority,
            v18_checker=v18_checker,
            v17_checker=v17_checker,
            v16_checker=v16_checker,
        )


# RT14 resolves V17 during ordinary function execution immediately after module
# import.  Bootstrap eagerly, but only through the verified closure above.
_BOOTSTRAP_AUTHORITY = DeferredAuthorityLoader().load()
V17 = _BOOTSTRAP_AUTHORITY.v17_checker


def derive_class(ax: dict[str, Any]) -> str:
    """Delegate to authenticated v1.11 semantics."""
    return _BOOTSTRAP_AUTHORITY.v111_checker.derive_class(ax)


def derive_codes(ax: dict[str, Any], maps: dict[str, Any]) -> dict[str, Any]:
    """Delegate to authenticated v1.11 semantics."""
    return _BOOTSTRAP_AUTHORITY.v111_checker.derive_codes(ax, maps)


def reduce_concurrent(conditions: dict[str, Any],
                      precedence: list[str]) -> dict[str, Any]:
    """Delegate to authenticated v1.11's v1.8-equivalent reducer."""
    return _BOOTSTRAP_AUTHORITY.v111_checker.reduce_concurrent(
        conditions, precedence)


def check(candidate: object, predecessor: object, v16: object) -> list[str]:
    """Exact frozen-RT14 three-argument compatibility adapter.

    The authority arguments must be byte-semantically equal to the pinned v1.7
    and v1.6 snapshots.  This public function intentionally does not validate
    the v1.12 successor artifact; the CLI uses ``_check_contract`` for that.
    """
    authority = _BOOTSTRAP_AUTHORITY
    if not isinstance(predecessor, dict) or predecessor != authority.v17:
        return ["D30-COMPAT-AUTHORITY: predecessor is not pinned v1.7 data"]
    if not isinstance(v16, dict) or v16 != authority.v16:
        return ["D30-COMPAT-AUTHORITY: retained input is not pinned v1.6 data"]
    return authority.v111_checker.check(candidate, predecessor, v16)


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
        "id": "D9-V112-HASH-BEFORE-EXECUTION",
        "transitiveInputs": [
            {"path": name, "sha256": digest, "role": ROLES[name]}
            for name, digest in PINS.items()
        ],
        "requiredOrder": [
            "read every artifact, checker and review input as inert bytes",
            "verify every byte snapshot against its pinned SHA-256 and abort the whole load on any mismatch",
            "parse pinned data snapshots and validate the exact v1.11 REJECT review, blocker and complete start/end hash window without importing executable dependencies",
            "only after every pin and rejection binding is clean invoke the injectable authority-import callback",
            "compile and execute only already-verified checker byte snapshots; require the executed v1.11 authority closure to expose the same authenticated v1.10-to-v1.6 module chain",
        ],
        "failureRule": (
            "Any read, pin, parse, v1.11-review verdict/blocker/hash-window, or "
            "executed-snapshot-closure failure prevents the authority-import "
            "callback or public API publication."
        ),
        "probe": (
            "The v1.12 selftest corrupts every one of the 19 pinned inputs and "
            "requires zero callback invocations; separate path, pyc and sys.modules "
            "probes require execution only from verified source snapshots."
        ),
    }


def _representation_disposition(authority: Authority) -> dict[str, Any]:
    return {
        "status": "V1.11-REJECTED / CANONICAL-RAW-REPRESENTATION-REPAIRED",
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
        "authorshipDisclosure": (
            "The v1.12 candidate and checker author also authored the independent "
            "v1.11 rejection review. That review is pinned repair input, not "
            "independent approval of v1.12; a different agent must review the "
            "exact v1.12 bytes."
        ),
        "correctedV111Claim": (
            "v1.11 preserved parsed semantics and repaired the complete RT14 "
            "runtime surface, but its statement that it retained inherited bytes "
            "exactly was false. v1.12 claims only the canonical raw identity and "
            "semantic/API properties mechanically checked below; it does not "
            "accept v1.11."
        ),
        "canonicalRawContract": {
            "invariantId": "D33-CANONICAL-RAW-PRESERVATION",
            "encoding": "UTF-8",
            "serializationFormula": (
                "json.dumps(obj, indent=2, ensure_ascii=True, "
                "sort_keys=False) + '\\n'"
            ),
            "fullCandidateRule": (
                "The exact candidate file bytes must equal the canonical "
                "serialization of the mechanically constructed exact v1.12 "
                "ordered object. This binds whitespace, newline, key order, "
                "escapes and values together."
            ),
            "v110Control": {
                "artifact": V110,
                "sha256": PINS[V110],
                "canonicalSerializationReproducesExactBytes": True,
            },
            "protectedUnchangedTopLevelRoots": copy.deepcopy(
                PROTECTED_RAW_ROOTS),
            "protectedInheritedArrayPrefixes": copy.deepcopy(
                PROTECTED_ARRAY_PREFIXES),
            "reviewIdentifiedLexicalLeaves": [
                path for path, _guardian in LEXICAL_LEAVES
            ],
            "requiredEscapedCodePoints": {
                "U+2014": 16,
                "U+2192": 1,
            },
            "rawProjectionRule": (
                "Every protected top-level value span and inherited array-prefix "
                "element is byte-identical to pinned v1.10; parsed equality is "
                "checked separately and cannot substitute for this raw comparison."
            ),
            "mutationRule": (
                "Replacing any protected escape with literal UTF-8, changing "
                "whitespace, final newline, key order or an inherited value must "
                "produce D33-CANONICAL-RAW-PRESERVATION. Substring counts are "
                "diagnostic only and never the oracle."
            ),
        },
        "retainedRuntimeSurface": _consumer_surface(authority),
        "semanticBoundary": (
            "No taxonomy, class, code, exit, axis, union, map, precedence, reducer, "
            "golden, matrix, identity, generic scope, provenance disclaimer or "
            "remedy change is permitted."
        ),
        "authorityBoundary": (
            "CANDIDATE-NOT-APPLIED / NO RT15, E8, OP6, product, TM, claim, "
            "narrative, integration, application or seal authority"
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
    "A different agent who authored neither v1.12 nor its checker must verify "
    "stable input hashes, exact ordered-object projections, canonical full-file "
    "bytes, every protected raw span and lexical leaf, the complete AST-derived "
    "frozen RT14 runtime surface, authenticated source snapshots, predecessor "
    "suites and the disposable RT14 API probe. The v1.12 author also authored "
    "the v1.11 rejection review and cannot approve this successor."
)
KNOWN_RESIDUAL = (
    "v1.11 remains rejected and is retained only as runtime/semantic lineage plus "
    "repair input. v1.12 is author-produced, not independently reviewed or applied; "
    "no RT15 exists, and E8, RT14 and OP6 remain unrejoined. Checker greenness is "
    "checker-scope evidence only and grants no product, integration, application "
    "or seal authority."
)


def _expected_successor(predecessor: dict[str, Any],
                        authority: Authority) -> dict[str, Any]:
    expected = copy.deepcopy(predecessor)
    expected["version"] = EXPECTED_VERSION
    expected["status"] = EXPECTED_STATUS
    expected["supersedes"] = PREDECESSOR
    expected["purpose"] = EXPECTED_PURPOSE
    expected["checkerTrustOrderContract"] = _trust_contract()
    expected[V110_COMPATIBILITY_KEY]["retainedFindingBoundary"] = \
        V110_RETAINED_BOUNDARY
    expected = _insert_after(expected, V110_COMPATIBILITY_KEY, [
        (COMPATIBILITY_KEY, _representation_disposition(authority)),
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


def _project_v111(candidate: dict[str, Any],
                  predecessor: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(candidate)
    projected.pop(COMPATIBILITY_KEY)
    for key in ("version", "status", "supersedes", "purpose"):
        projected[key] = copy.deepcopy(predecessor[key])
    for key in ("checkerTrustOrderContract", V110_COMPATIBILITY_KEY,
                "referenceDerivation", "conformanceClaims",
                "peerReviewRequired", "knownLimitations"):
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


def _canonical_json(value: Any) -> bytes:
    """The one admitted v1.12 JSON byte representation."""
    return (json.dumps(
        value, indent=2, ensure_ascii=True, sort_keys=False, allow_nan=False
    ) + "\n").encode("utf-8")


def _top_level_raw_value(source: bytes, key: str) -> bytes:
    """Extract one exact top-level JSON value span without reserializing it."""
    text = source.decode("utf-8")
    needle = f'  {json.dumps(key, ensure_ascii=True)}:'
    positions: list[int] = []
    start = 0
    while True:
        found = text.find(needle, start)
        if found < 0:
            break
        if found == 2 or text[found - 1] == "\n":
            positions.append(found)
        start = found + len(needle)
    if len(positions) != 1:
        raise ValueError(f"top-level raw member {key!r} count={len(positions)}")
    value_start = positions[0] + len(needle)
    while value_start < len(text) and text[value_start].isspace():
        value_start += 1
    _value, value_end = json.JSONDecoder().raw_decode(text, value_start)
    return text[value_start:value_end].encode("utf-8")


def _array_raw_elements(raw_value: bytes) -> list[bytes]:
    text = raw_value.decode("utf-8")
    if not text.startswith("["):
        raise ValueError("raw value is not an array")
    decoder = json.JSONDecoder()
    index = 1
    result: list[bytes] = []
    while True:
        while index < len(text) and text[index].isspace():
            index += 1
        if index < len(text) and text[index] == "]":
            return result
        if result:
            if index >= len(text) or text[index] != ",":
                raise ValueError("array delimiter missing")
            index += 1
            while index < len(text) and text[index].isspace():
                index += 1
        start = index
        _value, index = decoder.raw_decode(text, index)
        result.append(text[start:index].encode("utf-8"))


def _first_byte_difference(actual: bytes, expected: bytes) -> str:
    for index, (left, right) in enumerate(zip(actual, expected)):
        if left != right:
            return f"byte {index}: 0x{left:02x} != 0x{right:02x}"
    if len(actual) != len(expected):
        return f"length {len(actual)} != {len(expected)}"
    return "no difference"


def _raw_preservation_findings(candidate_source: object,
                               candidate: dict[str, Any],
                               expected: dict[str, Any],
                               authority: Authority) -> list[str]:
    """Compare actual bytes, canonical expected bytes, and predecessor spans."""
    prefix = "D33-CANONICAL-RAW-PRESERVATION"
    if not isinstance(candidate_source, bytes):
        return [f"{prefix}: exact candidate source bytes are required"]
    findings: list[str] = []
    try:
        expected_raw = _canonical_json(expected)
        actual_canonical = _canonical_json(candidate)
    except (TypeError, ValueError) as exc:
        return [f"{prefix}: candidate cannot be canonically serialized "
                f"({type(exc).__name__})"]
    if candidate_source != expected_raw:
        findings.append(
            f"{prefix}: file differs from exact canonical v1.12; "
            f"{_first_byte_difference(candidate_source, expected_raw)}")
    if candidate_source != actual_canonical:
        findings.append(
            f"{prefix}: file is not canonical serialization of its parsed object; "
            f"{_first_byte_difference(candidate_source, actual_canonical)}")

    v110_source = authority.snapshots[V110]
    if _canonical_json(authority.v110) != v110_source:
        findings.append(
            f"{prefix}: pinned v1.10 canonical-serialization control failed")
    try:
        projected_v111 = _project_v111(candidate, authority.predecessor)
        projected_v110 = authority.v111_checker._project_v110(
            projected_v111, authority.v111_authority.predecessor)
        if _canonical_json(projected_v110) != v110_source:
            findings.append(
                f"{prefix}: full canonical v1.10 projection is not byte-identical")
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        findings.append(
            f"{prefix}: cannot construct full canonical v1.10 projection "
            f"({type(exc).__name__})")
    successful_guardians: set[str] = set()
    for key in PROTECTED_RAW_ROOTS:
        try:
            actual_span = _top_level_raw_value(candidate_source, key)
            predecessor_span = _top_level_raw_value(v110_source, key)
        except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
            findings.append(
                f"{prefix}: cannot extract protected root {key} "
                f"({type(exc).__name__})")
            continue
        if actual_span != predecessor_span:
            findings.append(
                f"{prefix}: protected root {key} is not byte-identical to v1.10")
        else:
            successful_guardians.add(key)
    for key, indexes in PROTECTED_ARRAY_PREFIXES.items():
        try:
            actual_rows = _array_raw_elements(
                _top_level_raw_value(candidate_source, key))
            predecessor_rows = _array_raw_elements(
                _top_level_raw_value(v110_source, key))
            for index in indexes:
                guardian = f"{key}[{index}]"
                if actual_rows[index] != predecessor_rows[index]:
                    findings.append(
                        f"{prefix}: protected element {guardian} is not "
                        "byte-identical to v1.10")
                else:
                    successful_guardians.add(guardian)
        except (IndexError, UnicodeError, ValueError,
                json.JSONDecodeError) as exc:
            findings.append(
                f"{prefix}: cannot extract protected prefix {key} "
                f"({type(exc).__name__})")

    missing_leaf_guards = [
        path for path, guardian in LEXICAL_LEAVES
        if guardian not in successful_guardians
    ]
    if missing_leaf_guards:
        findings.append(
            f"{prefix}: {len(missing_leaf_guards)} review-identified lexical "
            "leaves lack a byte-identical guardian")
    # Counts are diagnostics after exact full-file and span comparisons; they
    # are deliberately not the raw-preservation oracle.
    if candidate_source.count(b"\\u2014") != 16 or \
            candidate_source.count(b"\\u2192") != 1 or \
            b"\xe2\x80\x94" in candidate_source or \
            b"\xe2\x86\x92" in candidate_source:
        findings.append(
            f"{prefix}: repaired lexical code-point diagnostics drifted")
    return findings


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
    module = types.ModuleType("opensip_d9_v112_public_api_view")
    module.check = check
    module.derive_class = derive_class
    module.derive_codes = derive_codes
    module.reduce_concurrent = reduce_concurrent
    module.V17 = V17
    return module


def _check_contract(candidate: object, authority: Authority,
                    candidate_source: object = None) -> list[str]:
    if not isinstance(candidate, dict) or not candidate:
        return ["D9-TOTALITY-ROOT: v1.12 candidate must be a nonempty object"]
    findings: list[str] = []
    try:
        expected = _expected_successor(authority.predecessor, authority)
        try:
            projected = _project_v111(candidate, authority.predecessor)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
            findings.append(
                f"D34-PROJECTION: cannot project v1.12 to v1.11 "
                f"({type(exc).__name__})")
            projected = None
        if projected is not None:
            difference = _first_difference(projected, authority.predecessor)
            if difference:
                findings.append(
                    "D34-PROJECTION: v1.12 does not project exactly to pinned "
                    f"v1.11; first difference: {difference}")
            retained = authority.v111_checker._check_contract(
                projected, authority.v111_authority)
            findings.extend(f"D0..D32 retained checker: {item}" for item in retained)

        actual_calls = _enumerate_rt14_calls(authority.snapshots[RT14_CHECKER])
        if actual_calls != EXPECTED_CALL_SITES:
            findings.append(
                "D30-AST-SURFACE: pinned RT14 call surface differs from exact "
                "six-site authority")
        disposition = candidate.get(COMPATIBILITY_KEY)
        declared_surface = disposition.get("retainedRuntimeSurface") \
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
                findings.append(f"D34-NONEXPANSION: {key} changed")
        difference = _first_difference(candidate, expected)
        if difference:
            findings.append(
                "D35-EXACT-DELTA: candidate differs outside the closed v1.12 "
                f"successor; first difference: {difference}")
        findings.extend(_raw_preservation_findings(
            candidate_source, candidate, expected, authority))
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
    value = _disposition(root)["retainedRuntimeSurface"]
    if not isinstance(value, dict):
        raise TypeError("retainedRuntimeSurface")
    return value


def _canonical_contract(root: dict[str, Any]) -> dict[str, Any]:
    value = _disposition(root)["canonicalRawContract"]
    if not isinstance(value, dict):
        raise TypeError("canonicalRawContract")
    return value


def _named(rows: list[dict[str, Any]], name: str) -> dict[str, Any]:
    return next(row for row in rows if row.get("name") == name)


def _remove_named(rows: list[dict[str, Any]], name: str) -> None:
    rows.remove(_named(rows, name))


Mutation = tuple[str, Callable[[dict[str, Any]], None]]
MUTATIONS: list[Mutation] = [
    ("version", lambda root: root.__setitem__("version", "v1.11")),
    ("status promotion", lambda root: root.__setitem__("status", "APPLIED")),
    ("wrong supersedes", lambda root: root.__setitem__("supersedes", V110)),
    ("drop v1.11 disposition", lambda root: root.pop(COMPATIBILITY_KEY)),
    ("accept v1.11", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("reviewVerdict", "PASS")),
    ("wrong v1.11 artifact pin", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("artifactSha256", "0" * 64)),
    ("wrong v1.11 checker pin", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("checkerSha256", "0" * 64)),
    ("wrong v1.11 review pin", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("independentReviewSha256", "0" * 64)),
    ("wrong blocking finding", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("blockingFinding", "NONE")),
    ("hide authorship", lambda root: _disposition(root).__setitem__("authorshipDisclosure", "independent author")),
    ("restore false v1.11 claim", lambda root: _disposition(root).__setitem__("correctedV111Claim", "v1.11 retained bytes exactly")),
    ("change canonical formula", lambda root: _canonical_contract(root).__setitem__("serializationFormula", "json.dumps(obj)")),
    ("drop protected raw root", lambda root: _canonical_contract(root)["protectedUnchangedTopLevelRoots"].pop()),
    ("drop lexical leaf", lambda root: _canonical_contract(root)["reviewIdentifiedLexicalLeaves"].pop()),
    ("weaken raw rule", lambda root: _canonical_contract(root).__setitem__("rawProjectionRule", "parsed equality")),
    ("incomplete call enumeration", lambda root: _surface(root)["callSites"].pop()),
    ("fabricated call enumeration", lambda root: _surface(root)["callSites"].append({"line": 999, "path": "other", "positionalArity": 0, "keywordNames": []})),
    ("drop V17 declaration", lambda root: _remove_named(_surface(root)["requiredTopLevelExports"], "V17")),
    ("wrong V17 kind", lambda root: _named(_surface(root)["requiredTopLevelExports"], "V17").__setitem__("kind", "callable")),
    ("drop check declaration", lambda root: _remove_named(_surface(root)["requiredTopLevelExports"], "check")),
    ("wrong check arity", lambda root: _named(_surface(root)["requiredTopLevelExports"], "check").__setitem__("positionalArity", 2)),
    ("extra consumer export", lambda root: _surface(root)["requiredTopLevelExports"].append({"name": "trusted", "kind": "callable", "positionalArity": 0})),
    ("drop V16 chain", lambda root: _surface(root)["requiredChainedExports"].pop(0)),
    ("wrong chained derive", lambda root: _surface(root)["requiredChainedExports"][1].__setitem__("path", "V17.derive_class")),
    ("broaden repair", lambda root: _disposition(root).__setitem__("semanticBoundary", "change taxonomy")),
    ("claim RT15", lambda root: _disposition(root).__setitem__("authorityBoundary", "RT15 APPLIED")),
    ("drop trust contract", lambda root: root.pop("checkerTrustOrderContract")),
    ("change v1.11 pin", lambda root: root["checkerTrustOrderContract"]["transitiveInputs"][0].__setitem__("sha256", "0" * 64)),
    ("drop inherited pin", lambda root: root["checkerTrustOrderContract"]["transitiveInputs"].pop()),
    ("execute before verify", lambda root: root["checkerTrustOrderContract"]["requiredOrder"].reverse()),
    ("old reference", lambda root: root["referenceDerivation"].__setitem__("implementation", "artifacts/check-d9-v1.11.py")),
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
    module_name = "opensip_check_d9_v111_verified"
    prior = sys.modules.get(module_name)
    hostile = types.ModuleType(module_name)
    hostile.V17 = object()
    sys.modules[module_name] = hostile
    try:
        _, _, loaded = loader.invoke_verified(_execute_verified_v111)
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
    with tempfile.TemporaryDirectory(prefix="opensip-d9-v112-env-") as raw:
        directory = pathlib.Path(raw)
        for name, source in trusted.items():
            (directory / name).write_bytes(source)
        marker = directory / "path-marker"
        malicious = trusted[PREDECESSOR_CHECKER] + (
            f"\npathlib.Path({str(marker)!r}).write_text('PATH')\n".encode())
        (directory / PREDECESSOR_CHECKER).write_bytes(malicious)
        try:
            _execute_snapshot("d9_v111_malicious_control",
                              PREDECESSOR_CHECKER, malicious)
            control_fired = marker.exists()
        except Exception:
            control_fired = False
        marker.unlink(missing_ok=True)

        def trusted_reader(path: pathlib.Path) -> bytes:
            return trusted[path.name]

        try:
            DeferredAuthorityLoader(directory).invoke_verified(
                _execute_verified_v111, trusted_reader)
            isolated = not marker.exists()
        except AuthorityLoadError:
            isolated = False
        probes.append(("verified snapshot defeats disk path swap",
                       control_fired and isolated))

        (directory / PREDECESSOR_CHECKER).write_bytes(
            trusted[PREDECESSOR_CHECKER])
        pyc_marker = directory / "pyc-marker"
        tag = sys.implementation.cache_tag or "python"
        pyc = directory / "__pycache__" / f"check-d9-v1.11.{tag}.pyc"
        _write_pyc(pyc, pyc_marker)
        try:
            importlib.machinery.SourcelessFileLoader(
                "d9_v111_malicious_pyc_control", str(pyc)).load_module()
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
        module = types.ModuleType("d9_v112_surface_probe")
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


def _semantic_runtime_probes(candidate: dict[str, Any]
                             ) -> tuple[list[tuple[str, bool]], int, int]:
    """Execute every retained golden and the exact four-row RT14 matrix."""
    probes: list[tuple[str, bool]] = []
    goldens = candidate.get("goldenCases")
    golden_count = len(goldens) if isinstance(goldens, list) else 0
    if not isinstance(goldens, list) or golden_count != 45:
        probes.append(("exactly 45 retained golden rows", False))
    else:
        for row in goldens:
            passed = False
            label = str(row.get("id", "?")) if isinstance(row, dict) else "?"
            try:
                axes = copy.deepcopy(row["scenarioAxes"])
                derived = {
                    "class": derive_class(copy.deepcopy(axes)),
                    **derive_codes(copy.deepcopy(axes), candidate["codeMaps"]),
                }
                expected = {
                    key: row["expectedTermination"][key]
                    for key in ("class", "errorCode", "reasonCodes")
                    if key in row["expectedTermination"]
                }
                passed = derived == expected and \
                    candidate["classToExitCode"].get(derived["class"]) is not None
            except (AttributeError, IndexError, KeyError, TypeError, ValueError):
                passed = False
            probes.append((f"golden {label}", passed))

    try:
        matrix = candidate["hostDerivedUnsatisfiableFinalizationContract"][
            "retainedCoreCompletionMatrix"]
    except (KeyError, TypeError):
        matrix = None
    matrix_count = len(matrix) if isinstance(matrix, list) else 0
    if not isinstance(matrix, list) or matrix_count != 4:
        probes.append(("exactly four retained CoreCompletion context rows", False))
    else:
        for row in matrix:
            passed = False
            label = str(row.get("id", "?")) if isinstance(row, dict) else "?"
            try:
                axes = copy.deepcopy(row["axes"])
                derived = {
                    "class": derive_class(copy.deepcopy(axes)),
                    **derive_codes(copy.deepcopy(axes), candidate["codeMaps"]),
                }
                expected = {
                    key: row["expectedTermination"][key]
                    for key in ("class", "errorCode", "reasonCodes")
                    if key in row["expectedTermination"]
                }
                passed = derived == expected and \
                    candidate["classToExitCode"][derived["class"]] == \
                    row["expectedExitCode"]
            except (AttributeError, IndexError, KeyError, TypeError, ValueError):
                passed = False
            probes.append((f"CoreCompletion context {label}", passed))
    return probes, golden_count, matrix_count


def _value_at(root: Any, accessor: tuple[object, ...]) -> Any:
    value = root
    for component in accessor:
        value = value[component]
    return value


def _lexical_raw_mutations(candidate: dict[str, Any],
                           source: bytes) -> list[tuple[str, bytes]]:
    """Mutate each review-identified inherited escape independently."""
    mutations: list[tuple[str, bytes]] = []
    declared_paths = [path for path, _guardian in LEXICAL_LEAVES]
    if set(declared_paths) != set(LEXICAL_ACCESSORS):
        raise ValueError("lexical accessor coverage drifted")
    for path in declared_paths:
        value = _value_at(candidate, LEXICAL_ACCESSORS[path])
        if not isinstance(value, str):
            raise TypeError(f"lexical leaf {path} is not a string")
        encoded = json.dumps(value, ensure_ascii=True).encode("utf-8")
        if source.count(encoded) != 1:
            raise ValueError(f"lexical leaf {path} raw value is not unique")
        escape = b"\\u2192" if "\u2192" in value else b"\\u2014"
        literal = b"\xe2\x86\x92" if escape == b"\\u2192" else b"\xe2\x80\x94"
        if encoded.count(escape) != 1:
            raise ValueError(f"lexical leaf {path} escape count drifted")
        changed_value = encoded.replace(escape, literal, 1)
        mutations.append((
            f"escape-to-literal {path}",
            source.replace(encoded, changed_value, 1),
        ))
    return mutations


def _raw_representation_mutations(candidate: dict[str, Any],
                                  source: bytes) -> list[tuple[str, bytes]]:
    mutations = _lexical_raw_mutations(candidate, source)
    if not source.startswith(b"{\n") or not source.endswith(b"\n"):
        raise ValueError("canonical source anchors absent")
    reordered = copy.deepcopy(candidate)
    first_key = next(iter(reordered))
    first_value = reordered.pop(first_key)
    reordered[first_key] = first_value
    changed_value = copy.deepcopy(candidate)
    changed_value["classToExitCode"]["success"] = 99
    mutations.extend([
        ("top-level whitespace", source.replace(b"{\n", b"{ \n", 1)),
        ("missing final newline", source[:-1]),
        ("CRLF newlines", source.replace(b"\n", b"\r\n")),
        ("extra final newline", source + b"\n"),
        ("top-level key order", _canonical_json(reordered)),
        ("protected inherited value", _canonical_json(changed_value)),
    ])
    return mutations


def _raw_mutation_probes(candidate: dict[str, Any], source: bytes,
                         authority: Authority) -> list[tuple[str, bool]]:
    probes: list[tuple[str, bool]] = []
    try:
        mutations = _raw_representation_mutations(candidate, source)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        return [(f"raw mutation construction ({type(exc).__name__})", False)]
    for name, changed_source in mutations:
        passed = False
        try:
            if changed_source == source:
                raise ValueError("raw mutation was a no-op")
            changed = _parse_json_bytes(changed_source, name)
            findings = _check_contract(changed, authority, changed_source)
            passed = any(item.startswith(
                "D33-CANONICAL-RAW-PRESERVATION") for item in findings)
        except (AuthorityLoadError, TypeError, ValueError):
            passed = False
        probes.append((name, passed))
    return probes


def _dirty_base_refusal_probe(candidate: dict[str, Any], source: bytes,
                              authority: Authority) -> bool:
    """Prove a valid-JSON dirty base cannot enter mutation testing as clean."""
    if not source.startswith(b"{\n"):
        return False
    dirty_source = source.replace(b"{\n", b"{ \n", 1)
    dirty = _parse_json_bytes(dirty_source, "dirty-base-probe")
    findings = _check_contract(dirty, authority, dirty_source)
    return dirty_source != source and any(item.startswith(
        "D33-CANONICAL-RAW-PRESERVATION") for item in findings)


def _rt14_rebind_probe() -> tuple[bool, str]:
    """Run an honest disposable RT14 checker-API compatibility probe."""
    checker_digest = hashlib.sha256((HERE / CHECKER).read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix="opensip-d9-v112-rt14-") as raw:
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
        rebound_checker = directory / "check-retention-custody-v14-d9-v112-sim.py"
        rebound_checker.write_text(rebound_source)

        candidate = json.loads((directory / RT14).read_text())
        authority_row = candidate["contextualD9Rejoin"]["authority"]
        authority_row["d9Checker"] = CHECKER
        authority_row["d9CheckerSha256"] = checker_digest
        rebound_candidate = directory / "retention-tiers.v14-d9-v112-sim.json"
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


def selftest(candidate: dict[str, Any], candidate_source: bytes,
             authority: Authority, loader: DeferredAuthorityLoader) -> int:
    # This is intentionally the first invariant: no mutation result can mask a
    # dirty base, and parsed equality cannot stand in for the candidate bytes.
    expected = _expected_successor(authority.predecessor, authority)
    expected_source = _canonical_json(expected)
    if candidate_source != expected_source or \
            candidate_source != _canonical_json(candidate):
        print("REFUSING to self-test: base is not the exact canonical v1.12 bytes")
        for finding in _raw_preservation_findings(
                candidate_source, candidate, expected, authority)[:12]:
            print("  -", finding)
        return 1

    base_findings = _check_contract(candidate, authority, candidate_source)
    if base_findings:
        print(f"REFUSING to self-test: base has {len(base_findings)} finding(s)")
        for finding in base_findings[:12]:
            print("  -", finding)
        return 1
    try:
        dirty_base_passed = _dirty_base_refusal_probe(
            candidate, candidate_source, authority)
    except (AuthorityLoadError, TypeError, ValueError):
        dirty_base_passed = False
    print("canonical base and dirty-base refusal")
    print(f"  {'pass' if dirty_base_passed else 'FAIL':>6}  "
          "valid-JSON noncanonical base is refused before mutations")
    if not dirty_base_passed:
        return 1

    projected = _project_v111(candidate, authority.predecessor)
    print("\nretained v1.11/v1.10/v1.9/v1.8/v1.7/v1.6 mutation proofs")
    if authority.v111_checker.selftest(
            projected, authority.v111_authority,
            authority.v111_checker.DeferredAuthorityLoader()) != 0:
        return 1

    print("\nv1.12 closed-successor object mutations — every row must be REJECTED\n")
    escaped = 0
    for name, mutate in MUTATIONS:
        changed = copy.deepcopy(candidate)
        before = copy.deepcopy(changed)
        try:
            mutate(changed)
            if changed == before:
                raise ValueError("mutation did not change candidate")
            findings = _check_contract(
                changed, authority, _canonical_json(changed))
            structural = [item for item in findings if not item.startswith(
                "D33-CANONICAL-RAW-PRESERVATION")]
        except Exception as exc:
            structural = []
            print(f"  ESCAPE  {name}\n          harness raised {type(exc).__name__}")
            escaped += 1
            continue
        if not structural:
            escaped += 1
        print(f"  {'reject' if structural else 'ESCAPE':>6}  {name}")
        print(f"          {structural[0] if structural else 'NO STRUCTURAL FINDING'}")

    raw_probes = _raw_mutation_probes(candidate, candidate_source, authority)
    raw_failures = sum(0 if passed else 1 for _name, passed in raw_probes)
    print("\nv1.12 raw-representation mutations — every row must raise D33\n")
    for name, passed in raw_probes:
        print(f"  {'pass' if passed else 'FAIL':>6}  {name}")

    semantic, golden_count, matrix_count = _semantic_runtime_probes(candidate)
    sections: list[tuple[str, list[tuple[str, bool]]]] = [
        ("trust-order", _trust_order_probes(loader)),
        ("AST consumer-surface", _ast_probes(authority)),
        ("runtime surface mutations", _runtime_mutation_probes(authority)),
        ("45-golden/four-row runtime semantics", semantic),
        ("malicious environment", _environment_probes(loader)),
    ]
    probe_failures = 0
    probe_count = 0
    for label, probes in sections:
        print(f"\nv1.12 {label} probes — every row must PASS\n")
        for name, passed in probes:
            probe_count += 1
            probe_failures += 0 if passed else 1
            print(f"  {'pass' if passed else 'FAIL':>6}  {name}")

    print("\nv1.12 hostile parsed shapes — every row must be REJECTED\n")
    hostile_failures = 0
    hostile = _hostile_candidates(candidate)
    for name, value in hostile:
        try:
            try:
                hostile_source = _canonical_json(value)
            except (TypeError, ValueError):
                hostile_source = b""
            findings = _check_contract(value, authority, hostile_source)
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
    if escaped or raw_failures or probe_failures or hostile_failures or \
            not rebind_passed or golden_count != 45 or matrix_count != 4:
        print(
            f"v1.12 failures: {escaped}/{len(MUTATIONS)} object mutations "
            f"escaped; {raw_failures}/{len(raw_probes)} raw mutations failed; "
            f"{probe_failures}/{probe_count} probes failed; "
            f"{hostile_failures}/{len(hostile)} hostile shapes escaped; "
            f"goldens={golden_count}/45; context rows={matrix_count}/4; "
            f"RT14 API probe={'pass' if rebind_passed else 'FAIL'}")
        return 1
    print(
        f"all {len(MUTATIONS)} object and {len(raw_probes)} raw mutations "
        f"rejected; {probe_count} trust/AST/runtime/semantic/environment probes "
        f"passed, including {golden_count} goldens and {matrix_count} context "
        f"rows; {len(hostile)} hostile shapes rejected; every retained "
        "predecessor suite passed; disposable RT14 checker-API normal+selftest "
        "passed")
    return 0


def main() -> int:
    positional = [argument for argument in sys.argv[1:]
                  if argument != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        candidate, candidate_source = load_source(path)
    except (OSError, AuthorityLoadError, UnicodeError, json.JSONDecodeError,
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
        return selftest(candidate, candidate_source, authority, loader)

    findings = _check_contract(candidate, authority, candidate_source)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    print(
        f"D9 v1.12 contract OK — {path.name}, exact canonical raw bytes, "
        "exact v1.11 ordered projection, 6 frozen RT14 call sites, "
        f"{len(TOP_LEVEL_EXPORTS)} top-level and {len(CHAINED_EXPORTS)} chained "
        f"exports resolved, {len(PINS)} pins verified before import, retained "
        "D0..D32 clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
