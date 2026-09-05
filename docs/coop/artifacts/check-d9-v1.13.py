#!/usr/bin/env python3
"""Isolated-launch successor checker for the D9 v1.13 candidate.

Caller-owned ``python3 -I -B`` startup is the trust root.  The in-script guard
only refuses an unsupported invocation once control reaches this source; it
cannot undo interpreter or site activity that happened before line 1.

The exact v1.12 checker and its REJECT review are authenticated repair inputs.
v1.13 changes launch/trust/review metadata and checker invocation mechanics
only.  It preserves v1.12's raw representation repair, complete frozen RT14
API and all retained D9 semantics.

Authorship disclosure: this checker author also authored the independent v1.12
REJECT review.  A different agent must review the exact v1.13 bytes.

Supported usage only:
  python3 -I -B artifacts/check-d9-v1.13.py [contract] [--selftest]
Exit: 0 clean; 1 findings; 2 unsupported invocation/input/JSON error.
"""
from __future__ import annotations

import sys

_STARTUP_REFUSAL = (
    "D9V113-UNSUPPORTED-INVOCATION: caller must use python3 -I -B "
    "artifacts/check-d9-v1.13.py"
)
if sys.flags.isolated != 1:
    print(_STARTUP_REFUSAL, file=sys.stderr)
    raise SystemExit(2)

import ast
import copy
import hashlib
import importlib.util
import inspect
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import types
from typing import Any, Callable, Mapping


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "d9-exit-contract.v1.13.json"
CHECKER = "check-d9-v1.13.py"
PREDECESSOR = "d9-exit-contract.v1.12.json"
PREDECESSOR_CHECKER = "check-d9-v1.12.py"
PREDECESSOR_REVIEW = \
    "d9-exit-contract.v1.12.review-independent-prefreeze.json"
V110 = "d9-exit-contract.v1.10.json"
V18 = "d9-exit-contract.v1.8.json"
V18_CHECKER = "check-d9-v1.8.py"
RT14 = "retention-tiers.v14.json"
RT14_CHECKER = "check-retention-custody-v14.py"

EXPECTED_VERSION = "v1.13"
EXPECTED_STATUS = (
    "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW "
    "(v1.13 caller-owned isolated-launch repair over rejected v1.12)"
)
EXPECTED_PURPOSE = (
    "Total host-owned process-exit contract: preserve v1.12 canonical raw, "
    "frozen-RT14 API and D9 semantic repairs while making caller-owned "
    "python3 -I -B startup the explicit checker trust root."
)
REFERENCE_IMPLEMENTATION = (
    "artifacts/check-d9-v1.13.py::"
    "check+derive_class+derive_codes+reduce_concurrent+V17.V16.derive_class"
)
NORMAL_COMMAND = "python3 -I -B artifacts/check-d9-v1.13.py"
SELFTEST_COMMAND = \
    "python3 -I -B artifacts/check-d9-v1.13.py --selftest"
EXPECTED_CLAIM = (
    "Under the sole admitted caller-owned isolated invocation, the exact "
    "ordered v1.13 object projects to rejected v1.12, every inherited protected "
    "raw span remains byte-identical, and the complete frozen RT14 API and D9 "
    "semantics remain authenticated and behaviorally unchanged."
)
COMPATIBILITY_KEY = "v112StartupDisposition"
REJECTION_ID = "D9V112-PF-01-PREAUTH-PYTHONPATH-EXECUTION"
STARTUP_REFUSAL = _STARTUP_REFUSAL

INHERITED_PINS: dict[str, str] = {
    "d9-exit-contract.v1.11.json": "09ab6b579173bdbd9575d46e7df96b8279a0bb12512638e25ad56e28d16e9895",
    "check-d9-v1.11.py": "9b637adee48432bb5388ce51212d59a1965044d2c1d5f6b6a4a3dd8ed519000a",
    "d9-exit-contract.v1.11.review-independent-prefreeze.json": "df1e89324a6c7645e96f69a2cc924731e4e37eeea64c10058cdd4cfcdfdbbcec",
    "d9-exit-contract.v1.10.json": "bf1d7eb0ab24de89f665f46c25377195a2721fc7fcb62f3aa449d0887b705b7b",
    "check-d9-v1.10.py": "77f86334a0ee016960224880fe75ef2b9b44d3adf20799c8354e992fbf19cca6",
    "d9-exit-contract.v1.10.review-independent-prefreeze.json": "7faefdf8f2c19e39ad9fdd6fba8df6f08c586aa73b7e5ab7ed917ae4c223e476",
    "d9-exit-contract.v1.9.json": "bc3c2b48d3615bc262166a698d3a3559bc2fa2fbd2f637de0dbf943309194404",
    "check-d9-v1.9.py": "956e41e279e758af5dd5e342a5404f334f6223add72abdb1340c85fafa2bd936",
    "d9-exit-contract.v1.9.review-independent-prefreeze.json": "409e55ddcc2121da5624a112728cd2d126586411a9abe06435c64d1c02b71373",
    "d9-exit-contract.v1.8.json": "5fb5466372da7c8ef935a1233eb67869f21c3cdb21d67b3767159998ad26a30d",
    "check-d9-v1.8.py": "827e5bdd600e2682d7653bc738f07efe066f90f4d7db7bad16a7f7fd5eb91e47",
    "d9-exit-contract.v1.8.review-independent-prefreeze.json": "f044620aaac0ea4f7efc6bdd51983278bf5858f5f967b6d48310e7c0139fedb9",
    "d9-exit-contract.v1.7.json": "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    "check-d9-v1.7.py": "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
    "d9-exit-contract.v1.6.json": "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    "check-d9.py": "9f8e16a0000e59d2f1326f97f1b8afcc5c7121eb0c57b6c440d76b9c401346a7",
    "retention-tiers.v14.json": "b66d0275d326cdd0cfdbec5e0810788e7768c10c9f1d7ab2c4df8c44b6975770",
    "check-retention-custody-v14.py": "6b190a89ba1700cf820746b473e8e3a521c9b2f6b4856f0c501d72a44b0a1d60",
    "retention-tiers.v14.review-independent-prefreeze.json": "dfb037bd121f7b73fbfeb77bbbaf0e1028a8c89318c5991bb3b3ec935046575c",
}
PINS: dict[str, str] = {
    PREDECESSOR: "17aa2161619ca6abae209dd2b2eda3a16d533718f1697cc31b87325feaa4b2d4",
    PREDECESSOR_CHECKER: "32566f4f56d81ead4e3f2582ef3a6e934ca1fa0ca4172b13124e952018ec9c8a",
    PREDECESSOR_REVIEW: "1e6486db60e24a6ba9eef06ca8c2808a09376917189dd330f7808567fe31bd4c",
    **INHERITED_PINS,
}
ROLES = {
    PREDECESSOR: "rejected v1.12 candidate projected at the ordered-object boundary",
    PREDECESSOR_CHECKER: "retained executable v1.12 raw/API/semantic authority",
    PREDECESSOR_REVIEW: "independent v1.12 REJECT and isolated-launch repair authority",
    **{name: "v1.12-declared authenticated transitive input"
       for name in INHERITED_PINS},
}

PYTHON_ENV_PREFIX = "PYTHON"
ISOLATED_PREFIX = [sys.executable, "-I", "-B"]
NEGATIVE_PREFIX = [sys.executable, "-B"]


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


def _execute_verified_v112(
        snapshots: Mapping[str, bytes], _parsed: Mapping[str, Any]
) -> tuple[types.ModuleType, Any]:
    module = _execute_snapshot(
        "opensip_check_d9_v112_verified", PREDECESSOR_CHECKER,
        snapshots[PREDECESSOR_CHECKER])
    if dict(getattr(module, "PINS", {})) != INHERITED_PINS:
        raise AuthorityLoadError("v1.12 executable transitive pin set drifted")
    authority = getattr(module, "_BOOTSTRAP_AUTHORITY", None)
    inherited = getattr(authority, "snapshots", None)
    if not isinstance(inherited, Mapping) or any(
            inherited.get(name) != snapshots[name] for name in INHERITED_PINS):
        raise AuthorityLoadError(
            "executed v1.12 authority did not use the outer verified snapshots")
    return module, authority


class Authority:
    def __init__(self, *, snapshots: Mapping[str, bytes],
                 predecessor: dict[str, Any],
                 predecessor_review: dict[str, Any],
                 v112_checker: types.ModuleType, v112_authority: Any):
        self.snapshots = snapshots
        self.predecessor = predecessor
        self.predecessor_review = predecessor_review
        self.v112_checker = v112_checker
        self.v112_authority = v112_authority


ReadBytes = Callable[[pathlib.Path], bytes]
ImportCallback = Callable[[Mapping[str, bytes], Mapping[str, Any]], Any]


class DeferredAuthorityLoader:
    """Verify the complete repair closure before retained source execution."""

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
            raise AuthorityLoadError("pinned v1.12 review is not the exact REJECT")
        expected_window = {
            PREDECESSOR: PINS[PREDECESSOR],
            PREDECESSOR_CHECKER: PINS[PREDECESSOR_CHECKER],
            **INHERITED_PINS,
        }
        window = review.get("hashWindow") or {}
        if window.get("startEqualsEnd") is not True or \
                window.get("inputHashDrift") is not False or \
                window.get("start") != expected_window or \
                window.get("end") != expected_window:
            raise AuthorityLoadError("v1.12 review hash window does not bind all inputs")
        subjects = {
            row.get("path"): row.get("sha256")
            for row in (review.get("reviewBinding") or {}).get(
                "exactSubjects", []) if isinstance(row, dict)
        }
        if subjects != {
                PREDECESSOR: PINS[PREDECESSOR],
                PREDECESSOR_CHECKER: PINS[PREDECESSOR_CHECKER]}:
            raise AuthorityLoadError("v1.12 review exactSubjects drifted")
        blockers = [
            row.get("id") for row in review.get("blockingFindings", [])
            if isinstance(row, dict)
        ]
        if blockers != [REJECTION_ID]:
            raise AuthorityLoadError("v1.12 review blocker drifted")
        return parsed

    def invoke_verified(self, callback: ImportCallback,
                        byte_reader: ReadBytes | None = None
                        ) -> tuple[Mapping[str, bytes], Mapping[str, Any], Any]:
        snapshots = self._snapshots(byte_reader)
        parsed = self._parsed(snapshots)
        result = callback(snapshots, parsed)
        return snapshots, parsed, result

    def load(self) -> Authority:
        snapshots, parsed, loaded = self.invoke_verified(_execute_verified_v112)
        if not isinstance(loaded, tuple) or len(loaded) != 2 or \
                not isinstance(loaded[0], types.ModuleType):
            raise AuthorityLoadError("verified importer did not return v1.12 authority")
        return Authority(
            snapshots=snapshots,
            predecessor=parsed[PREDECESSOR],
            predecessor_review=parsed[PREDECESSOR_REVIEW],
            v112_checker=loaded[0],
            v112_authority=loaded[1],
        )


# This eager bootstrap is reached only after the caller-owned isolated-start
# guard above. Every retained source byte is pinned before it executes.
_BOOTSTRAP_AUTHORITY = DeferredAuthorityLoader().load()
V17 = _BOOTSTRAP_AUTHORITY.v112_checker.V17


def derive_class(ax: dict[str, Any]) -> str:
    return _BOOTSTRAP_AUTHORITY.v112_checker.derive_class(ax)


def derive_codes(ax: dict[str, Any], maps: dict[str, Any]) -> dict[str, Any]:
    return _BOOTSTRAP_AUTHORITY.v112_checker.derive_codes(ax, maps)


def reduce_concurrent(conditions: dict[str, Any],
                      precedence: list[str]) -> dict[str, Any]:
    return _BOOTSTRAP_AUTHORITY.v112_checker.reduce_concurrent(
        conditions, precedence)


def check(candidate: object, predecessor: object, v16: object) -> list[str]:
    """Exact frozen-RT14 three-argument compatibility adapter."""
    return _BOOTSTRAP_AUTHORITY.v112_checker.check(
        candidate, predecessor, v16)


def _trust_contract() -> dict[str, Any]:
    return {
        "id": "D9-V113-ISOLATED-HASH-BEFORE-EXECUTION",
        "startupTrustRoot": {
            "owner": "caller",
            "soleAdmittedPrefix": ["python3", "-I", "-B"],
            "normalCommand": NORMAL_COMMAND,
            "selftestCommand": SELFTEST_COMMAND,
            "requiredInterpreterFlags": {
                "isolated": 1,
                "ignoreEnvironment": 1,
                "noUserSite": 1,
            },
            "boundary": (
                "Caller-owned isolated startup is the prevention boundary. "
                "Script code cannot undo interpreter or site activity that "
                "occurred before line 1."
            ),
            "earlyRefusal": {
                "id": "D9V113-UNSUPPORTED-INVOCATION",
                "exit": 2,
                "rule": (
                    "After the required future import, import only built-in sys; "
                    "if sys.flags.isolated != 1, emit the stable refusal and exit "
                    "before every other explicit import and eager bootstrap."
                ),
                "scope": (
                    "Diagnostic and defense-in-depth refusal only; not retroactive "
                    "prevention of nonisolated interpreter startup."
                ),
            },
        },
        "transitiveInputs": [
            {"path": name, "sha256": digest, "role": ROLES[name]}
            for name, digest in PINS.items()
        ],
        "requiredOrder": [
            "caller starts the checker with the exact isolated -I -B prefix",
            "the checker confirms sys.flags.isolated before any non-sys explicit import or eager bootstrap",
            "read every artifact, checker and review input as inert bytes",
            "verify every byte snapshot against its pinned SHA-256 and abort the whole load on any mismatch",
            "parse pinned data and validate the exact v1.12 REJECT review, blocker and complete start/end hash window",
            "only after every pin and rejection binding is clean execute the already-verified v1.12 checker source buffer",
            "require the executed v1.12 authority closure to expose the identical authenticated inherited snapshots",
        ],
        "childProcessRule": {
            "authorityBearingPrefix": ["sys.executable", "-I", "-B"],
            "environment": (
                "Remove all environment entries whose names start PYTHON for "
                "authority-bearing, retained-predecessor and disposable RT14 children."
            ),
            "retainedHarnessRule": (
                "The v1.13 harness interposes one closed launcher over authenticated "
                "v1.12/v1.11 selftest subprocess calls; it inserts -I, preserves -B, "
                "sanitizes PYTHON* and rejects non-Python child commands."
            ),
            "negativeControlException": {
                "count": 1,
                "argv": ["sys.executable", "-B", "check-d9-v1.13.py"],
                "environment": "all PYTHON* entries removed; controlled cwd",
                "requiredResult": "exit 2 with exact D9V113-UNSUPPORTED-INVOCATION line",
                "authority": "NONE; cannot contribute pass or verification evidence",
            },
            "environmentIsolationControl": (
                "One isolated -I -B child deliberately receives a benign local "
                "PYTHONPATH marker fixture and must leave the marker absent."
            ),
        },
        "failureRule": (
            "Unsupported startup refuses before bootstrap. Any read, pin, parse, "
            "review-binding or verified-snapshot closure failure prevents public "
            "authority. No nonisolated child can contribute authority."
        ),
    }


def _startup_disposition() -> dict[str, Any]:
    return {
        "status": "V1.12-REJECTED / CALLER-OWNED-ISOLATED-LAUNCH-REPAIRED",
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
            "The v1.13 candidate/checker author also authored the independent "
            "v1.12 REJECT review. That review is pinned repair input, not "
            "independent approval of v1.13; a different agent must review v1.13."
        ),
        "correctedBoundary": (
            "v1.12 proved its authenticated-buffer, pin, review, pyc, path and "
            "sys.modules properties after trustworthy interpreter startup. It did "
            "not establish process-start isolation under its declared python3 -B "
            "command. v1.13 makes caller-owned -I -B the explicit trust root."
        ),
        "isolatedLaunchContract": copy.deepcopy(
            _trust_contract()["startupTrustRoot"]),
        "childProcessContract": copy.deepcopy(
            _trust_contract()["childProcessRule"]),
        "reviewEvidence": {
            "nonisolatedV112Control": (
                "The pinned review observed its benign local process-start marker "
                "before v1.12 returned success under python3 -B."
            ),
            "isolatedV112Control": (
                "The pinned review observed the same marker absent and normal "
                "success under python3 -I -B."
            ),
            "v113RequiredControls": [
                "clean nonisolated exact refusal with no authority",
                "isolated benign-PYTHONPATH marker remains absent",
                "every authority-bearing child begins sys.executable -I -B",
                "every authority-bearing child environment contains no PYTHON* key",
            ],
        },
        "representationCarryForward": {
            "v113ToV112Projection": (
                "Remove this disposition and restore the exact v1.12 successor "
                "metadata/trust/review fields; ordered object equality is required."
            ),
            "canonicalSerialization": (
                "json.dumps(obj, indent=2, ensure_ascii=True, "
                "sort_keys=False) + '\\n'"
            ),
            "protectedRawSource": (
                "Pinned v1.12 v111RepresentationDisposition.canonicalRawContract"
            ),
            "requiredEscapedCodePoints": {"U+2014": 16, "U+2192": 1},
        },
        "semanticBoundary": (
            "No taxonomy, class, code, exit, axis, union, map, precedence, "
            "reducer, golden, matrix, identity, generic scope, provenance "
            "disclaimer, remedy or frozen RT14 API change is permitted."
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
    "A different agent who authored neither v1.13 nor its checker nor the v1.12 "
    "REJECT review must verify stable hashes, exact ordered/raw projections, "
    "the process-start -I boundary, early nonisolated refusal, every nested "
    "child argv/environment, retained v1.12 suites, complete frozen RT14 API, "
    "semantic identity, hostile-shape totality and disposable RT14 normal plus "
    "selftest before any application."
)
KNOWN_RESIDUAL = (
    "v1.12 remains rejected and is retained only as raw/API/semantic lineage "
    "plus repair input. v1.13 is author-produced, not independently reviewed "
    "or applied; no accepted RT15 exists and E8/OP6 remain unrejoined. Caller "
    "ownership of isolated startup is an explicit precondition. Checker "
    "greenness grants no product, integration, application or seal authority."
)


def _expected_successor(predecessor: dict[str, Any]) -> dict[str, Any]:
    expected = copy.deepcopy(predecessor)
    expected["version"] = EXPECTED_VERSION
    expected["status"] = EXPECTED_STATUS
    expected["supersedes"] = PREDECESSOR
    expected["purpose"] = EXPECTED_PURPOSE
    expected["checkerTrustOrderContract"] = _trust_contract()
    expected = _insert_after(expected, "v111RepresentationDisposition", [
        (COMPATIBILITY_KEY, _startup_disposition()),
    ])
    expected["referenceDerivation"]["implementation"] = \
        REFERENCE_IMPLEMENTATION
    expected["conformanceClaims"] = [{
        "claim": EXPECTED_CLAIM,
        "reproduce": NORMAL_COMMAND,
        "mutationProof": SELFTEST_COMMAND,
    }]
    expected["peerReviewRequired"][-1] = PEER_REVIEW
    expected["knownLimitations"][-1] = KNOWN_RESIDUAL
    return expected


def _project_v112(candidate: dict[str, Any],
                  predecessor: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(candidate)
    projected.pop(COMPATIBILITY_KEY)
    for key in (
            "version", "status", "supersedes", "purpose",
            "checkerTrustOrderContract", "referenceDerivation",
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
    return None if actual == expected else f"{path}: {actual!r} != {expected!r}"


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(
        value, indent=2, ensure_ascii=True, sort_keys=False, allow_nan=False
    ) + "\n").encode("utf-8")


def _raw_findings(candidate_source: object, candidate: dict[str, Any],
                  expected: dict[str, Any], authority: Authority) -> list[str]:
    prefix = "D36-CANONICAL-RAW-PRESERVATION"
    if not isinstance(candidate_source, bytes):
        return [f"{prefix}: exact candidate source bytes are required"]
    findings: list[str] = []
    try:
        expected_source = _canonical_json(expected)
        actual_canonical = _canonical_json(candidate)
    except (TypeError, ValueError) as exc:
        return [f"{prefix}: cannot serialize candidate ({type(exc).__name__})"]
    if candidate_source != expected_source:
        findings.append(f"{prefix}: file differs from exact canonical v1.13")
    if candidate_source != actual_canonical:
        findings.append(f"{prefix}: file is not canonical serialization of its object")
    predecessor_source = authority.snapshots[PREDECESSOR]
    if _canonical_json(authority.predecessor) != predecessor_source:
        findings.append(f"{prefix}: pinned v1.12 canonical control failed")
    try:
        projected = _project_v112(candidate, authority.predecessor)
        if _canonical_json(projected) != predecessor_source:
            findings.append(f"{prefix}: canonical v1.12 projection is not exact")
        helpers = authority.v112_checker
        for key in helpers.PROTECTED_RAW_ROOTS:
            if helpers._top_level_raw_value(candidate_source, key) != \
                    helpers._top_level_raw_value(predecessor_source, key):
                findings.append(f"{prefix}: protected root {key} drifted")
        for key, indexes in helpers.PROTECTED_ARRAY_PREFIXES.items():
            actual = helpers._array_raw_elements(
                helpers._top_level_raw_value(candidate_source, key))
            prior = helpers._array_raw_elements(
                helpers._top_level_raw_value(predecessor_source, key))
            for index in indexes:
                if actual[index] != prior[index]:
                    findings.append(
                        f"{prefix}: protected element {key}[{index}] drifted")
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        findings.append(f"{prefix}: raw projection raised {type(exc).__name__}")
    if candidate_source.count(b"\\u2014") != 16 or \
            candidate_source.count(b"\\u2192") != 1 or \
            b"\xe2\x80\x94" in candidate_source or \
            b"\xe2\x86\x92" in candidate_source:
        findings.append(f"{prefix}: inherited lexical diagnostics drifted")
    return findings


def _public_api_view() -> types.ModuleType:
    module = types.ModuleType("opensip_d9_v113_public_api_view")
    module.check = check
    module.derive_class = derive_class
    module.derive_codes = derive_codes
    module.reduce_concurrent = reduce_concurrent
    module.V17 = V17
    return module


def _startup_source_findings(source: bytes) -> list[str]:
    findings: list[str] = []
    try:
        tree = ast.parse(source.decode("utf-8"), filename=CHECKER)
    except (UnicodeError, SyntaxError) as exc:
        return [f"D37-STARTUP-SOURCE: cannot parse checker ({type(exc).__name__})"]
    body = tree.body
    imports = [node for node in body if isinstance(node, (ast.Import, ast.ImportFrom))]
    sys_import = next((node for node in imports if isinstance(node, ast.Import)
                       and [alias.name for alias in node.names] == ["sys"]), None)
    guard = next((node for node in body if isinstance(node, ast.If)
                  and ast.unparse(node.test) == "sys.flags.isolated != 1"), None)
    if sys_import is None or guard is None:
        return ["D37-STARTUP-SOURCE: exact sys import/isolated guard absent"]
    intervening = [node for node in imports
                   if sys_import.lineno < node.lineno < guard.lineno]
    if intervening:
        findings.append("D37-STARTUP-SOURCE: import occurs before isolated guard")
    later_imports = [node for node in imports if node is not sys_import and
                     not (isinstance(node, ast.ImportFrom) and
                          node.module == "__future__")]
    if any(node.lineno < guard.lineno for node in later_imports):
        findings.append("D37-STARTUP-SOURCE: non-sys import precedes guard")
    has_refusal = any(isinstance(node, ast.Call) and
                      isinstance(node.func, ast.Name) and node.func.id == "print"
                      for node in ast.walk(guard))
    has_exit = any(isinstance(node, ast.Raise) and
                   "SystemExit(2)" in ast.unparse(node)
                   for node in ast.walk(guard))
    if not has_refusal or not has_exit:
        findings.append("D37-STARTUP-SOURCE: guard lacks exact refusal/exit")
    bootstrap_line = next((node.lineno for node in body if isinstance(node, ast.Assign)
                           and any(isinstance(target, ast.Name) and
                                   target.id == "_BOOTSTRAP_AUTHORITY"
                                   for target in node.targets)), None)
    if bootstrap_line is None or bootstrap_line <= guard.lineno:
        findings.append("D37-STARTUP-SOURCE: bootstrap is not after guard")
    return findings


def _check_contract(candidate: object, authority: Authority,
                    candidate_source: object = None) -> list[str]:
    if not isinstance(candidate, dict) or not candidate:
        return ["D9-TOTALITY-ROOT: v1.13 candidate must be a nonempty object"]
    findings: list[str] = []
    try:
        expected = _expected_successor(authority.predecessor)
        try:
            projected = _project_v112(candidate, authority.predecessor)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
            findings.append(
                f"D38-PROJECTION: cannot project to v1.12 ({type(exc).__name__})")
            projected = None
        if projected is not None:
            difference = _first_difference(projected, authority.predecessor)
            if difference:
                findings.append(
                    f"D38-PROJECTION: v1.13 is not exact v1.12; {difference}")
            retained = authority.v112_checker._check_contract(
                projected, authority.v112_authority, _canonical_json(projected))
            findings.extend(f"D0..D35 retained checker: {item}" for item in retained)
        difference = _first_difference(candidate, expected)
        if difference:
            findings.append(f"D39-EXACT-DELTA: unauthorized delta; {difference}")
        if (sys.flags.isolated, sys.flags.ignore_environment,
                sys.flags.no_user_site) != (1, 1, 1):
            findings.append(
                "D37-STARTUP-FLAGS: isolated/ignore_environment/no_user_site "
                "must all equal 1")
        source_findings = _startup_source_findings((HERE / CHECKER).read_bytes())
        findings.extend(source_findings)
        surface = authority.predecessor["v111RepresentationDisposition"][
            "retainedRuntimeSurface"]
        public = _public_api_view()
        findings.extend(authority.v112_checker._surface_resolution_findings(
            public, surface))
        findings.extend(authority.v112_checker._runtime_invocation_findings(
            public, authority.v112_authority))
        findings.extend(_raw_findings(
            candidate_source, candidate, expected, authority))
    except (AttributeError, IndexError, KeyError, StopIteration, TypeError,
            ValueError) as exc:
        findings.append(
            f"D9-TOTALITY-EXCEPTION: malformed parsed shape ({type(exc).__name__})")
    return findings


def _disposition(root: dict[str, Any]) -> dict[str, Any]:
    value = root[COMPATIBILITY_KEY]
    if not isinstance(value, dict):
        raise TypeError(COMPATIBILITY_KEY)
    return value


def _launch(root: dict[str, Any]) -> dict[str, Any]:
    value = _disposition(root)["isolatedLaunchContract"]
    if not isinstance(value, dict):
        raise TypeError("isolatedLaunchContract")
    return value


def _children(root: dict[str, Any]) -> dict[str, Any]:
    value = _disposition(root)["childProcessContract"]
    if not isinstance(value, dict):
        raise TypeError("childProcessContract")
    return value


Mutation = tuple[str, Callable[[dict[str, Any]], None]]
MUTATIONS: list[Mutation] = [
    ("version", lambda root: root.__setitem__("version", "v1.12")),
    ("status promotion", lambda root: root.__setitem__("status", "APPLIED")),
    ("wrong supersedes", lambda root: root.__setitem__("supersedes", V110)),
    ("drop v1.12 disposition", lambda root: root.pop(COMPATIBILITY_KEY)),
    ("accept v1.12", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("reviewVerdict", "PASS")),
    ("wrong v1.12 artifact pin", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("artifactSha256", "0" * 64)),
    ("wrong v1.12 checker pin", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("checkerSha256", "0" * 64)),
    ("wrong v1.12 review pin", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("independentReviewSha256", "0" * 64)),
    ("wrong v1.12 blocker", lambda root: _disposition(root)["rejectedCandidate"].__setitem__("blockingFinding", "NONE")),
    ("hide review authorship", lambda root: _disposition(root).__setitem__("authorshipDisclosure", "independent")),
    ("normal command drops -I", lambda root: _launch(root).__setitem__("normalCommand", "python3 -B artifacts/check-d9-v1.13.py")),
    ("selftest command drops -I", lambda root: _launch(root).__setitem__("selftestCommand", "python3 -B artifacts/check-d9-v1.13.py --selftest")),
    ("script owns trust", lambda root: _launch(root).__setitem__("owner", "script")),
    ("isolated flag false", lambda root: _launch(root)["requiredInterpreterFlags"].__setitem__("isolated", 0)),
    ("pre-line claim", lambda root: _launch(root).__setitem__("boundary", "script prevents startup hooks")),
    ("remove early refusal", lambda root: _launch(root).pop("earlyRefusal")),
    ("child drops -I", lambda root: _children(root).__setitem__("authorityBearingPrefix", ["sys.executable", "-B"])),
    ("child keeps PYTHONPATH", lambda root: _children(root).__setitem__("environment", "inherit environment")),
    ("broad negative exception", lambda root: _children(root)["negativeControlException"].__setitem__("count", 2)),
    ("negative grants authority", lambda root: _children(root)["negativeControlException"].__setitem__("authority", "PASS")),
    ("drop trust input", lambda root: root["checkerTrustOrderContract"]["transitiveInputs"].pop()),
    ("reverse trust order", lambda root: root["checkerTrustOrderContract"]["requiredOrder"].reverse()),
    ("old reference", lambda root: root["referenceDerivation"].__setitem__("implementation", "artifacts/check-d9-v1.12.py")),
    ("conformance drops -I", lambda root: root["conformanceClaims"][0].__setitem__("reproduce", "python3 -B artifacts/check-d9-v1.13.py")),
    ("drop peer review", lambda root: root["peerReviewRequired"].pop()),
    ("drop residual", lambda root: root["knownLimitations"].pop()),
    ("semantic exit drift", lambda root: root["classToExitCode"].__setitem__("success", 99)),
]


def _sanitized_env(base: Mapping[str, str] | None = None) -> dict[str, str]:
    source = dict(os.environ if base is None else base)
    return {key: value for key, value in source.items()
            if not key.upper().startswith(PYTHON_ENV_PREFIX)}


_ORIGINAL_SUBPROCESS_RUN = subprocess.run


def _isolated_command(command: Any) -> list[str]:
    if not isinstance(command, (list, tuple)) or not command or \
            os.fspath(command[0]) != sys.executable:
        raise RuntimeError("retained harness attempted a non-Python child")
    tail = [os.fspath(item) for item in command[1:]]
    while tail and tail[0] in ("-I", "-B"):
        tail.pop(0)
    return [sys.executable, "-I", "-B", *tail]


def _retained_v112_selftest(candidate: dict[str, Any],
                            authority: Authority
                            ) -> tuple[int, list[dict[str, Any]]]:
    child_log: list[dict[str, Any]] = []
    original = subprocess.run

    def isolated_run(command: Any, *args: Any, **kwargs: Any) -> Any:
        rewritten = _isolated_command(command)
        environment = _sanitized_env(kwargs.get("env"))
        kwargs["env"] = environment
        kwargs["shell"] = False
        child_log.append({
            "argv": rewritten[:3],
            "pythonEnvironmentKeys": sorted(
                key for key in environment if key.upper().startswith("PYTHON")),
        })
        return _ORIGINAL_SUBPROCESS_RUN(rewritten, *args, **kwargs)

    subprocess.run = isolated_run
    try:
        projected = _project_v112(candidate, authority.predecessor)
        result = authority.v112_checker.selftest(
            projected, authority.snapshots[PREDECESSOR],
            authority.v112_authority,
            authority.v112_checker.DeferredAuthorityLoader())
    finally:
        subprocess.run = original
    return result, child_log


def _clean_nonisolated_refusal() -> tuple[bool, str]:
    # Copy only the checker: the exact refusal must not need or read any pin.
    with tempfile.TemporaryDirectory(prefix="opensip-d9-v113-refusal-") as raw:
        directory = pathlib.Path(raw)
        isolated_checker = directory / CHECKER
        shutil.copy2(HERE / CHECKER, isolated_checker)
        command = [sys.executable, "-B", str(isolated_checker)]
        completed = _ORIGINAL_SUBPROCESS_RUN(
            command, cwd=directory, env=_sanitized_env(), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=30, check=False)
        exact = completed.stdout == "" and \
            completed.stderr == STARTUP_REFUSAL + "\n"
        return completed.returncode == 2 and exact, \
            f"rc={completed.returncode}, exact={exact}, pins-present=False"


def _isolated_environment_control() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="opensip-d9-v113-start-") as raw:
        directory = pathlib.Path(raw)
        marker = directory / "startup-marker"
        sitecustomize = directory / "sitecustomize.py"
        sitecustomize.write_text(
            "from pathlib import Path\n"
            f"Path({str(marker)!r}).write_text('LOCAL-MARKER')\n")
        environment = _sanitized_env()
        # Deliberately present only for this -I control. The isolated interpreter
        # must ignore it; authority-bearing production/probe children sanitize it.
        environment["PYTHONPATH"] = str(directory)
        completed = _ORIGINAL_SUBPROCESS_RUN(
            [sys.executable, "-I", "-B", str(HERE / CHECKER)],
            cwd=HERE, env=environment, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=30, check=False)
        passed = completed.returncode == 0 and not marker.exists() and \
            "D9 v1.13 contract OK" in completed.stdout
        return passed, f"rc={completed.returncode}, marker={marker.exists()}"


def _rt14_rebind_probe() -> tuple[bool, str, list[dict[str, Any]]]:
    checker_digest = hashlib.sha256((HERE / CHECKER).read_bytes()).hexdigest()
    child_log: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="opensip-d9-v113-rt14-") as raw:
        directory = pathlib.Path(raw) / "artifacts"
        directory.mkdir()
        for source in HERE.iterdir():
            if source.is_file():
                shutil.copy2(source, directory / source.name)
        frozen = (directory / RT14_CHECKER).read_text()
        name_line = 'D9_CHECKER = "check-d9-v1.8.py"'
        old_digest = INHERITED_PINS[V18_CHECKER]
        if frozen.count(name_line) != 1 or frozen.count(old_digest) != 1:
            return False, "RT14 replacement anchors drifted", child_log
        rebound = frozen.replace(
            name_line, f'D9_CHECKER = "{CHECKER}"', 1).replace(
                old_digest, checker_digest, 1)
        rebound_checker = directory / "check-retention-custody-v14-d9-v113-sim.py"
        rebound_checker.write_text(rebound)
        candidate = json.loads((directory / RT14).read_text())
        row = candidate["contextualD9Rejoin"]["authority"]
        row["d9Checker"] = CHECKER
        row["d9CheckerSha256"] = checker_digest
        rebound_candidate = directory / "retention-tiers.v14-d9-v113-sim.json"
        rebound_candidate.write_text(json.dumps(candidate, indent=2) + "\n")
        for extra in ([], ["--selftest"]):
            environment = _sanitized_env()
            command = [
                sys.executable, "-I", "-B", str(rebound_checker),
                str(rebound_candidate), *extra,
            ]
            child_log.append({
                "argv": command[:3],
                "pythonEnvironmentKeys": sorted(
                    key for key in environment
                    if key.upper().startswith("PYTHON")),
            })
            completed = _ORIGINAL_SUBPROCESS_RUN(
                command, cwd=directory, env=environment, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                timeout=240, check=False)
            if completed.returncode != 0:
                tail = "\n".join(completed.stdout.splitlines()[-12:])
                return False, f"RT14 {'selftest' if extra else 'normal'} failed: {tail}", child_log
        return True, "isolated RT14 normal and selftest passed", child_log


def _trust_order_probes(loader: DeferredAuthorityLoader
                        ) -> list[tuple[str, bool]]:
    probes: list[tuple[str, bool]] = []
    for target in PINS:
        invoked = 0

        def reader(path: pathlib.Path, name: str = target) -> bytes:
            source = path.read_bytes()
            return source + b"X" if path.name == name else source

        def marker(_snapshots: Mapping[str, bytes],
                   _parsed: Mapping[str, Any]) -> None:
            nonlocal invoked
            invoked += 1

        try:
            loader.invoke_verified(marker, reader)
            passed = False
        except AuthorityLoadError:
            passed = invoked == 0
        probes.append((target, passed))
    return probes


def _raw_mutations(candidate: dict[str, Any], source: bytes
                   ) -> list[tuple[str, bytes]]:
    rows: list[tuple[str, bytes]] = []
    for escape, literal, label in (
            (b"\\u2014", b"\xe2\x80\x94", "u2014"),
            (b"\\u2192", b"\xe2\x86\x92", "u2192")):
        offset = 0
        index = 0
        while True:
            found = source.find(escape, offset)
            if found < 0:
                break
            changed = source[:found] + literal + source[found + len(escape):]
            rows.append((f"{label}-{index}", changed))
            offset = found + len(escape)
            index += 1
    reordered = copy.deepcopy(candidate)
    first = next(iter(reordered))
    value = reordered.pop(first)
    reordered[first] = value
    rows.extend([
        ("whitespace", source.replace(b"{\n", b"{ \n", 1)),
        ("missing-newline", source[:-1]),
        ("extra-newline", source + b"\n"),
        ("crlf", source.replace(b"\n", b"\r\n")),
        ("key-order", _canonical_json(reordered)),
        ("escaped-key", source.replace(
            b'  "artifact":', b'  "\\u0061rtifact":', 1)),
    ])
    return rows


HOSTILE_ROOTS: list[tuple[str, Any]] = [
    ("null", None), ("false", False), ("zero", 0),
    ("float", 1.5), ("string", "hostile"), ("array", []),
    ("empty-object", {}), ("array-object", [{}]),
]


def _hostile_candidates(candidate: dict[str, Any]) -> list[tuple[str, Any]]:
    rows = list(HOSTILE_ROOTS)
    for key in (
            "checkerTrustOrderContract", "v111RepresentationDisposition",
            COMPATIBILITY_KEY, "exitClasses", "referenceDerivation",
            "conformanceClaims", "goldenCases", "peerReviewRequired",
            "knownLimitations", "scenarioAxesSchema", "classToExitCode",
            "codeMaps", "causeModel", "concurrentConditionReducer",
            "hostDerivedUnsatisfiableFinalizationContract"):
        for value in (None, "hostile"):
            changed = copy.deepcopy(candidate)
            changed[key] = value
            rows.append((f"{key}={type(value).__name__}", changed))
    return rows


def selftest(candidate: dict[str, Any], candidate_source: bytes,
             authority: Authority, loader: DeferredAuthorityLoader) -> int:
    expected = _expected_successor(authority.predecessor)
    if candidate_source != _canonical_json(expected) or \
            candidate_source != _canonical_json(candidate):
        print("REFUSING to self-test: base is not exact canonical v1.13")
        return 1
    base = _check_contract(candidate, authority, candidate_source)
    if base:
        print(f"REFUSING to self-test: base has {len(base)} finding(s)")
        for finding in base[:10]:
            print("  -", finding)
        return 1
    dirty = candidate_source.replace(b"{\n", b"{ \n", 1)
    dirty_findings = _check_contract(
        _parse_json_bytes(dirty, "dirty"), authority, dirty)
    dirty_passed = dirty != candidate_source and any(
        row.startswith("D36-CANONICAL-RAW-PRESERVATION")
        for row in dirty_findings)
    print("isolated startup and canonical base")
    startup_flags = (sys.flags.isolated, sys.flags.ignore_environment,
                     sys.flags.no_user_site) == (1, 1, 1)
    print(f"  {'pass' if startup_flags else 'FAIL':>6}  "
          "isolated/ignore_environment/no_user_site flags are all 1")
    print(f"  {'pass' if dirty_passed else 'FAIL':>6}  dirty base rejected before mutations")
    if not dirty_passed:
        return 1

    print("\nretained v1.12 suite with closed isolated-child interposition")
    retained_result, retained_children = _retained_v112_selftest(
        candidate, authority)
    retained_children_ok = bool(retained_children) and all(
        row["argv"] == ISOLATED_PREFIX and not row["pythonEnvironmentKeys"]
        for row in retained_children)
    print(f"  {'pass' if retained_result == 0 else 'FAIL':>6}  retained v1.12 selftest")
    print(f"  {'pass' if retained_children_ok else 'FAIL':>6}  "
          f"{len(retained_children)} retained children isolated and sanitized")

    print("\nv1.13 object mutations - every row must have a structural finding")
    escaped = 0
    for name, mutate in MUTATIONS:
        changed = copy.deepcopy(candidate)
        before = copy.deepcopy(changed)
        try:
            mutate(changed)
            if changed == before:
                raise ValueError("mutation did not change candidate")
            findings = _check_contract(changed, authority, _canonical_json(changed))
            structural = [row for row in findings if not row.startswith(
                "D36-CANONICAL-RAW-PRESERVATION")]
        except Exception as exc:
            structural = []
            print(f"  ESCAPE  {name}: harness raised {type(exc).__name__}")
            escaped += 1
            continue
        if not structural:
            escaped += 1
        print(f"  {'reject' if structural else 'ESCAPE':>6}  {name}")

    raw_rows = _raw_mutations(candidate, candidate_source)
    raw_failures = 0
    print("\nv1.13 raw mutations - every row must raise D36")
    for name, changed_source in raw_rows:
        passed = False
        try:
            if changed_source == candidate_source:
                raise ValueError("raw mutation did not change candidate")
            changed = _parse_json_bytes(changed_source, name)
            findings = _check_contract(changed, authority, changed_source)
            passed = any(row.startswith(
                "D36-CANONICAL-RAW-PRESERVATION") for row in findings)
        except (AuthorityLoadError, TypeError, ValueError):
            passed = False
        raw_failures += 0 if passed else 1
        print(f"  {'pass' if passed else 'FAIL':>6}  {name}")

    trust = _trust_order_probes(loader)
    trust_failures = sum(0 if passed else 1 for _name, passed in trust)
    print(f"\ntrust order: {len(trust) - trust_failures}/{len(trust)} pin corruptions blocked before callback")

    clean_refusal, refusal_detail = _clean_nonisolated_refusal()
    isolated_control, isolated_detail = _isolated_environment_control()
    checker_source = (HERE / CHECKER).read_bytes()
    weakened_source = checker_source.replace(
        b"if sys.flags.isolated != 1:\n", b"if False:\n", 1)
    source_guard = bool(_startup_source_findings(weakened_source)) and \
        not _startup_source_findings(checker_source)
    print("\nprocess-start controls")
    print(f"  {'pass' if clean_refusal else 'FAIL':>6}  clean nonisolated refusal ({refusal_detail})")
    print(f"  {'pass' if isolated_control else 'FAIL':>6}  isolated PYTHONPATH marker control ({isolated_detail})")
    print(f"  {'pass' if source_guard else 'FAIL':>6}  startup guard source mutation rejected")

    hostile = _hostile_candidates(candidate)
    hostile_failures = 0
    for _name, value in hostile:
        try:
            try:
                source = _canonical_json(value)
            except (TypeError, ValueError):
                source = b""
            findings = _check_contract(value, authority, source)
        except Exception:
            findings = []
        hostile_failures += 0 if findings else 1
    print(f"\nhostile JSON shapes: {len(hostile) - hostile_failures}/{len(hostile)} rejected without escape")

    rt14_passed, rt14_detail, rt14_children = _rt14_rebind_probe()
    rt14_children_ok = len(rt14_children) == 2 and all(
        row["argv"] == ISOLATED_PREFIX and not row["pythonEnvironmentKeys"]
        for row in rt14_children)
    print("\ndisposable frozen RT14 checker-API probe")
    print(f"  {'pass' if rt14_passed else 'FAIL':>6}  {rt14_detail}")
    print(f"  {'pass' if rt14_children_ok else 'FAIL':>6}  RT14 children isolated and sanitized")

    failed = escaped or raw_failures or trust_failures or hostile_failures or \
        retained_result != 0 or not retained_children_ok or \
        not clean_refusal or not isolated_control or not source_guard or \
        not rt14_passed or not rt14_children_ok
    print()
    if failed:
        print(
            f"v1.13 failures: object={escaped}/{len(MUTATIONS)}, "
            f"raw={raw_failures}/{len(raw_rows)}, trust={trust_failures}/{len(trust)}, "
            f"hostile={hostile_failures}/{len(hostile)}, retained={retained_result}, "
            f"retainedChildren={retained_children_ok}, startup="
            f"{clean_refusal}/{isolated_control}/{source_guard}, "
            f"rt14={rt14_passed}/{rt14_children_ok}")
        return 1
    print(
        f"all {len(MUTATIONS)} object and {len(raw_rows)} raw mutations rejected; "
        f"{len(trust)} pin corruptions blocked; {len(hostile)} hostile shapes "
        f"rejected; clean nonisolated refusal and isolated environment control "
        f"passed; {len(retained_children)} retained and {len(rt14_children)} RT14 "
        "children used -I -B with sanitized environments; retained v1.12 suite "
        "and disposable RT14 normal+selftest passed")
    return 0


def main() -> int:
    authority = _BOOTSTRAP_AUTHORITY
    if "--emit-candidate" in sys.argv[1:]:
        sys.stdout.write(_canonical_json(
            _expected_successor(authority.predecessor)).decode("utf-8"))
        return 0
    positional = [argument for argument in sys.argv[1:]
                  if argument not in ("--selftest", "--emit-candidate")]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        candidate, candidate_source = load_source(path)
    except (OSError, AuthorityLoadError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError) as exc:
        print(f"cannot load D9 candidate: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2
    if "--selftest" in sys.argv[1:]:
        if not isinstance(candidate, dict):
            print("selftest requires an object root", file=sys.stderr)
            return 1
        return selftest(
            candidate, candidate_source, authority, DeferredAuthorityLoader())
    findings = _check_contract(candidate, authority, candidate_source)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    print(
        f"D9 v1.13 contract OK - {path.name}; isolated caller trust root; "
        "exact canonical raw bytes and v1.12 projection; complete frozen RT14 "
        f"API; {len(PINS)} pins verified before retained execution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
