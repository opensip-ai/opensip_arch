#!/usr/bin/env python3
"""API/coherence-only successor checker for the D9 v1.14 candidate.

Caller-owned ``python3 -I -B`` startup is the trust root.  The in-script guard
only refuses an unsupported invocation once control reaches this source; it
cannot undo interpreter or site activity that happened before line 1.

d9-exit-contract.v1.13.json and check-d9-v1.13.py PASSED independent review
with zero blocking findings.  A verdict binds the exact bytes reviewed, so the
two coherence defects a blind Consumer-B implementer litmus found afterwards
are repaired in this successor and never in place.  v1.13, its checker and its
review are byte-pinned, retained, authenticated repair inputs.

The two repaired defects:

  D9V113-CB-01  concurrentConditionGoldens[0].conditions.rejectionCauses
                carried "invalid-config", which is not a member of the closed
                scenarioAxesSchema.properties.rejectionCause enum (the member
                is "config-invalid").  The deeper defect is that no checker in
                the retained chain ever validated the cause values inside
                concurrentConditionGoldens.conditions against the closed axis
                enums, so any out-of-enum cause sat undetected.  v1.14 fixes
                the value and adds D40-CAUSE-VALUE-CLOSURE, which validates
                every value in every pre-reduction condition record found by a
                recursive scan of the whole contract.

  D9V113-CB-02  hostTerminationUnion.fieldTypes.details was typed only
                {"type": "object", "nullable": false}, so an implementer could
                not know what may or must appear inside it.  v1.14 gives it an
                explicit normative disposition: an OPEN diagnostic bag with NO
                semantic authority that may never be parsed for control flow,
                plus the mechanically checkable fact that no golden and no
                core-completion row uses it.  D41-DETAILS-DISPOSITION enforces
                the statement and its teeth.

No exit class, class-to-exit-code entry, code vocabulary, reason or error
code, scenario axis, HostTermination union field, code map, cause model,
precedence rule or golden expected termination changes.  D42 rederives all 45
goldens, 4 core-completion rows and 6 pre-reduction reduction records from the
v1.14 object and from pinned v1.13 and requires the two derivations to be
identical.

Authorship disclosure: this checker and the v1.14 candidate share one author.
A different agent must review the exact v1.14 bytes.

Supported usage only:
  python3 -I -B artifacts/check-d9-v1.14.py [contract] [--selftest]
Exit: 0 clean; 1 findings; 2 unsupported invocation/input/JSON error;
      3 --selftest refused because the base candidate is not clean.
"""
from __future__ import annotations

import sys

_STARTUP_REFUSAL = (
    "D9V114-UNSUPPORTED-INVOCATION: caller must use python3 -I -B "
    "artifacts/check-d9-v1.14.py"
)
if sys.flags.isolated != 1:
    print(_STARTUP_REFUSAL, file=sys.stderr)
    raise SystemExit(2)

import ast
import copy
import hashlib
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import types
from typing import Any, Callable, Mapping


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "d9-exit-contract.v1.14.json"
CHECKER = "check-d9-v1.14.py"
PREDECESSOR = "d9-exit-contract.v1.13.json"
PREDECESSOR_CHECKER = "check-d9-v1.13.py"
PREDECESSOR_REVIEW = \
    "d9-exit-contract.v1.13.review-independent-prefreeze.json"
V112 = "d9-exit-contract.v1.12.json"
RT14 = "retention-tiers.v14.json"
RT14_CHECKER = "check-retention-custody-v14.py"
V18_CHECKER = "check-d9-v1.8.py"

EXPECTED_VERSION = "v1.14"
EXPECTED_STATUS = (
    "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW "
    "(v1.14 API/coherence-only repair over independently passed v1.13)"
)
EXPECTED_PURPOSE = (
    "Total host-owned process-exit contract: preserve every v1.13 class, "
    "code, axis, union field, map, precedence rule, golden and frozen RT14 "
    "API unchanged while repairing the two Consumer-B coherence defects, the "
    "out-of-enum pre-reduction rejection cause and the contentless details "
    "field, and closing the validation gap that hid the first one."
)
REFERENCE_IMPLEMENTATION = (
    "artifacts/check-d9-v1.14.py::"
    "check+derive_class+derive_codes+reduce_concurrent+V17.V16.derive_class"
)
NORMAL_COMMAND = "python3 -I -B artifacts/check-d9-v1.14.py"
SELFTEST_COMMAND = "python3 -I -B artifacts/check-d9-v1.14.py --selftest"
EXPECTED_CLAIM = (
    "Under the sole admitted caller-owned isolated invocation, the exact "
    "ordered v1.14 object differs from the independently passed v1.13 object "
    "only in successor metadata and the two declared coherence repairs; every "
    "cause value in every pre-reduction condition record is a member of its "
    "closed axis enum; the HostTermination details field carries an explicit "
    "normative no-authority disposition; and all 45 goldens, 4 retained "
    "core-completion rows and 6 pre-reduction reduction records rederive "
    "identically to v1.13."
)
COMPATIBILITY_KEY = "v113CoherenceDisposition"
STARTUP_REFUSAL = _STARTUP_REFUSAL

# The exact 22 transitive inputs the pinned, independently passed v1.13
# checker declares.  v1.14 re-verifies every one of them itself and then
# requires the executed v1.13 closure to expose the identical byte snapshots.
INHERITED_PINS: dict[str, str] = {
    "d9-exit-contract.v1.12.json": "17aa2161619ca6abae209dd2b2eda3a16d533718f1697cc31b87325feaa4b2d4",
    "check-d9-v1.12.py": "32566f4f56d81ead4e3f2582ef3a6e934ca1fa0ca4172b13124e952018ec9c8a",
    "d9-exit-contract.v1.12.review-independent-prefreeze.json": "1e6486db60e24a6ba9eef06ca8c2808a09376917189dd330f7808567fe31bd4c",
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
    PREDECESSOR: "fc2c546a4cdbe2038f3a5db333ab9903d21ae9d6223777b139b58551fb2f2fae",
    PREDECESSOR_CHECKER: "a905ab0e4b932c2ef4c565e847a12cb398abf9cd7a74abd92f95cbc85ffc8717",
    PREDECESSOR_REVIEW: "88ab60efb21f603213ebff722f62f310b422f03981895e3f6779f2febe734c5b",
    **INHERITED_PINS,
}
ROLES = {
    PREDECESSOR: "independently passed v1.13 predecessor projected at the ordered-object boundary",
    PREDECESSOR_CHECKER: "retained executable v1.13 raw/API/semantic authority",
    PREDECESSOR_REVIEW: "independent v1.13 PASS binding the exact repaired-from bytes",
    **{name: "v1.13-declared authenticated transitive input"
       for name in INHERITED_PINS},
}

PYTHON_ENV_PREFIX = "PYTHON"
ISOLATED_PREFIX = [sys.executable, "-I", "-B"]

# ---------------------------------------------------------------------------
# Repair 1 constants: the closed pre-reduction cause-value closure.
# ---------------------------------------------------------------------------
REPAIR_ONE_ID = "D9V113-CB-01-OUT-OF-ENUM-REJECTION-CAUSE"
REPAIR_ONE_PATH = "$.concurrentConditionGoldens[0].conditions.rejectionCauses[0]"
V113_REJECTION_VALUE = "invalid-config"
V114_REJECTION_VALUE = "config-invalid"
# Condition-array name -> (axis property name, read the enum from items).
CONDITION_ARRAYS: dict[str, tuple[str, bool]] = {
    "faultCauses": ("faultCause", False),
    "rejectionCauses": ("rejectionCause", False),
    "deficiencies": ("deficiency", False),
    "secondaryDeficiencies": ("secondaryDeficiencies", True),
}
# A pre-reduction condition record is identified by the three PLURAL primary
# arrays, which are exactly concurrentConditionReducer.inputSchema.required.
# secondaryDeficiencies alone does not identify one: a reduced scenarioAxes
# record also carries that name, and its enum is already checked as an axis by
# the retained chain.
PRIMARY_CONDITION_ARRAYS = ("faultCauses", "rejectionCauses", "deficiencies")
# Sibling expectation keys -> the condition array whose axis bounds them.
EXPECT_FAMILY_KEYS = ("expectFamily", "expectedFamily")
EXPECT_CAUSE_KEYS = ("expectCause", "expectedCause")
EXPECT_SECONDARY_KEYS = ("expectSecondaries", "expectedSecondaries")
FAMILY_TO_ARRAY = {
    "faultCause": "faultCauses",
    "rejectionCause": "rejectionCauses",
    "deficiency": "deficiencies",
}
CAUSE_SENTINEL = "none"
EXPECTED_CONDITION_RECORDS = (
    "$.concurrentConditionGoldens[0].conditions",
    "$.concurrentConditionGoldens[1].conditions",
    "$.concurrentConditionGoldens[2].conditions",
    "$.concurrentConditionGoldens[3].conditions",
    "$.concurrentConditionGoldens[4].conditions",
    "$.hostDerivedUnsatisfiableFinalizationContract"
    ".faultPrecedenceControl.conditions",
)

# ---------------------------------------------------------------------------
# Repair 2 constants: the HostTermination details disposition.
# ---------------------------------------------------------------------------
REPAIR_TWO_ID = "D9V113-CB-02-DETAILS-WITHOUT-CONTENT-SCHEMA"
REPAIR_TWO_PATH = "$.hostTerminationUnion.fieldTypes.details"
DETAILS_FIELD = "details"
DETAILS_REQUIRED_TOKENS = (
    "MUST NOT be parsed for control flow",
    "no semantic authority",
)
DETAILS_DISPOSITION: dict[str, Any] = {
    "type": "object",
    "nullable": False,
    "closed": False,
    "semanticAuthority": "NONE",
    "controlFlowUse": "FORBIDDEN",
    "normativeRule": (
        "details is an OPEN diagnostic bag. Its interior key set is "
        "deliberately not closed and it MUST NOT be parsed for control flow. "
        "It carries no semantic authority: no class, exit code, error code, "
        "reason code, remedy, retry disposition, identity, coverage or "
        "postcondition may be read from it, and deleting it from any "
        "termination changes no value this contract derives."
    ),
    "producerRules": [
        "MUST be a JSON object whose members are JSON-serializable; NaN, "
        "Infinity and non-JSON values are forbidden inside it.",
        "MUST NOT reintroduce a forbidden or closed union field: no member "
        "named exitCode, and no member that restates or contradicts class, "
        "errorCode, reasonCodes, runId, executionId, coverageId or signal.",
        "MUST NOT be the only place a machine-actionable fact appears. "
        "Anything a caller must act on belongs in the closed union fields and "
        "the closed code vocabulary.",
        "MAY be omitted entirely. Absence and presence are equivalent for "
        "every derivation in this contract.",
    ],
    "consumerRules": [
        "MUST NOT branch on details, on any member of details, or on its "
        "presence or absence.",
        "MUST treat details as opaque human-facing diagnostics: log it, "
        "render it, attach it to a report.",
        "MUST NOT reject a termination because details carries an "
        "unrecognized member. unknownFieldPolicy=reject closes the union "
        "field set, not the interior of this bag.",
    ],
    "declaredOn": (
        "Optional on the request-rejected variant only. No variant requires "
        "it and no other variant permits it."
    ),
    "whyNotClosed": (
        "No golden case and no retained core-completion row carries details, "
        "so the corpus contains zero observed uses from which a closed "
        "content schema could be derived. Authoring one here would assert "
        "field semantics this contract has never exercised and would be a new "
        "unreviewed surface rather than a repair. The honest closure is to "
        "state that the field has no authority, not to guess its shape."
    ),
    "derivationIndependence": (
        "Mechanically checkable: details appears in zero "
        "goldenCases[*].expectedTermination and zero "
        "hostDerivedUnsatisfiableFinalizationContract"
        ".retainedCoreCompletionMatrix[*].expectedTermination, and the "
        "reference derivation emits only reasonCodes or errorCode, so no "
        "derived class, code list or exit code can depend on it."
    ),
    "repairedIn": (
        "v1.14. v1.13 typed this field only {type: object, nullable: false}, "
        "which told an implementer nothing about what may or must appear "
        "inside it. Silence was the defect; this statement, not a guessed "
        "closed schema, is the repair."
    ),
}

AUTHORIZED_METADATA_KEYS = (
    "version", "status", "supersedes", "purpose",
    "checkerTrustOrderContract", "referenceDerivation",
    "conformanceClaims", "peerReviewRequired", "knownLimitations",
)
REPAIRED_RAW_ROOTS = ("hostTerminationUnion", "concurrentConditionGoldens")
AUTHORIZED_SEMANTIC_DELTA_PATHS = (REPAIR_ONE_PATH, REPAIR_TWO_PATH)

RAW_PREFIX = "D36R-CANONICAL-RAW-PRESERVATION"
GOLDEN_COUNT = 45
MATRIX_COUNT = 4
REDUCTION_COUNT = 6


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


def _execute_verified_v113(
        snapshots: Mapping[str, bytes], _parsed: Mapping[str, Any]
) -> tuple[types.ModuleType, Any]:
    module = _execute_snapshot(
        "opensip_check_d9_v113_verified", PREDECESSOR_CHECKER,
        snapshots[PREDECESSOR_CHECKER])
    if dict(getattr(module, "PINS", {})) != INHERITED_PINS:
        raise AuthorityLoadError("v1.13 executable transitive pin set drifted")
    authority = getattr(module, "_BOOTSTRAP_AUTHORITY", None)
    inherited = getattr(authority, "snapshots", None)
    if not isinstance(inherited, Mapping) or any(
            inherited.get(name) != snapshots[name] for name in INHERITED_PINS):
        raise AuthorityLoadError(
            "executed v1.13 authority did not use the outer verified snapshots")
    return module, authority


class Authority:
    def __init__(self, *, snapshots: Mapping[str, bytes],
                 predecessor: dict[str, Any],
                 predecessor_review: dict[str, Any],
                 v113_checker: types.ModuleType, v113_authority: Any):
        self.snapshots = snapshots
        self.predecessor = predecessor
        self.predecessor_review = predecessor_review
        self.v113_checker = v113_checker
        self.v113_authority = v113_authority

    @property
    def helpers(self) -> types.ModuleType:
        """The authenticated v1.12 raw/surface helper module reached through v1.13."""
        return self.v113_checker._BOOTSTRAP_AUTHORITY.v112_checker

    @property
    def v112_authority(self) -> Any:
        return self.v113_checker._BOOTSTRAP_AUTHORITY.v112_authority


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
        if not isinstance(verdict, dict) or verdict.get("decision") != "PASS" or \
                verdict.get("blockingFindingCount") != 0 or \
                verdict.get("inputHashDrift") is not False or \
                verdict.get("candidateState") != "CANDIDATE-NOT-APPLIED":
            raise AuthorityLoadError(
                "pinned v1.13 review is not the exact zero-blocker PASS")
        if review.get("blockingFindings") != []:
            raise AuthorityLoadError("v1.13 review carries blocking findings")
        window = review.get("hashWindow") or {}
        start = window.get("start")
        end = window.get("end")
        if window.get("startEqualsEnd") is not True or \
                window.get("inputHashDrift") is not False or \
                not isinstance(start, dict) or start != end:
            raise AuthorityLoadError(
                "v1.13 review hash window is not an exact start=end window")
        for name in (PREDECESSOR, PREDECESSOR_CHECKER, *INHERITED_PINS):
            if start.get(name) != PINS[name]:
                raise AuthorityLoadError(
                    f"v1.13 review hash window does not bind {name}")
        subjects = {
            row.get("path"): row.get("sha256")
            for row in (review.get("reviewBinding") or {}).get(
                "exactSubjects", []) if isinstance(row, dict)
        }
        if subjects != {
                PREDECESSOR: PINS[PREDECESSOR],
                PREDECESSOR_CHECKER: PINS[PREDECESSOR_CHECKER]}:
            raise AuthorityLoadError("v1.13 review exactSubjects drifted")
        return parsed

    def invoke_verified(self, callback: ImportCallback,
                        byte_reader: ReadBytes | None = None
                        ) -> tuple[Mapping[str, bytes], Mapping[str, Any], Any]:
        snapshots = self._snapshots(byte_reader)
        parsed = self._parsed(snapshots)
        result = callback(snapshots, parsed)
        return snapshots, parsed, result

    def load(self) -> Authority:
        snapshots, parsed, loaded = self.invoke_verified(_execute_verified_v113)
        if not isinstance(loaded, tuple) or len(loaded) != 2 or \
                not isinstance(loaded[0], types.ModuleType):
            raise AuthorityLoadError("verified importer did not return v1.13 authority")
        return Authority(
            snapshots=snapshots,
            predecessor=parsed[PREDECESSOR],
            predecessor_review=parsed[PREDECESSOR_REVIEW],
            v113_checker=loaded[0],
            v113_authority=loaded[1],
        )


# This eager bootstrap is reached only after the caller-owned isolated-start
# guard above. Every retained source byte is pinned before it executes.
_BOOTSTRAP_AUTHORITY = DeferredAuthorityLoader().load()
V17 = _BOOTSTRAP_AUTHORITY.v113_checker.V17


def derive_class(ax: dict[str, Any]) -> str:
    return _BOOTSTRAP_AUTHORITY.v113_checker.derive_class(ax)


def derive_codes(ax: dict[str, Any], maps: dict[str, Any]) -> dict[str, Any]:
    return _BOOTSTRAP_AUTHORITY.v113_checker.derive_codes(ax, maps)


def reduce_concurrent(conditions: dict[str, Any],
                      precedence: list[str]) -> dict[str, Any]:
    return _BOOTSTRAP_AUTHORITY.v113_checker.reduce_concurrent(
        conditions, precedence)


def check(candidate: object, predecessor: object, v16: object) -> list[str]:
    """Exact frozen-RT14 three-argument compatibility adapter."""
    return _BOOTSTRAP_AUTHORITY.v113_checker.check(candidate, predecessor, v16)


# ---------------------------------------------------------------------------
# Derived successor construction.
# ---------------------------------------------------------------------------
def _trust_contract() -> dict[str, Any]:
    return {
        "id": "D9-V114-ISOLATED-HASH-BEFORE-EXECUTION",
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
                "id": "D9V114-UNSUPPORTED-INVOCATION",
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
        "exitCodes": {
            "0": "clean",
            "1": "findings",
            "2": "unsupported invocation, unreadable input or JSON error",
            "3": (
                "--selftest refused because the base candidate is not clean, "
                "so the mutation suite would not be an oracle over it. Exit 3 "
                "is distinct from green, from findings and from a bad "
                "invocation, and the refusal names the dirty base."
            ),
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
            "parse pinned data and validate the exact v1.13 zero-blocker PASS, its empty blocker list and its complete start/end hash window",
            "only after every pin and review binding is clean execute the already-verified v1.13 checker source buffer",
            "require the executed v1.13 authority closure to expose the identical authenticated inherited snapshots",
        ],
        "childProcessRule": {
            "authorityBearingPrefix": ["sys.executable", "-I", "-B"],
            "environment": (
                "Remove all environment entries whose names start PYTHON for "
                "authority-bearing, retained-predecessor and disposable RT14 children."
            ),
            "retainedHarnessRule": (
                "The v1.14 harness observes every child the authenticated v1.13 "
                "harness launches without rewriting its argv, so the reviewed "
                "v1.13 negative and marker controls keep their exact reviewed "
                "shape, and it requires the observed census to be the declared one."
            ),
            "negativeControlException": {
                "count": 1,
                "argv": ["sys.executable", "-B", "check-d9-v1.14.py"],
                "environment": "all PYTHON* entries removed; controlled cwd",
                "requiredResult": "exit 2 with exact D9V114-UNSUPPORTED-INVOCATION line",
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


def _coherence_disposition() -> dict[str, Any]:
    return {
        "status": (
            "V1.13-INDEPENDENTLY-PASSED / "
            "CONSUMER-B-COHERENCE-DEFECTS-REPAIRED-IN-SUCCESSOR"
        ),
        "passedPredecessor": {
            "artifact": PREDECESSOR,
            "artifactSha256": PINS[PREDECESSOR],
            "checker": PREDECESSOR_CHECKER,
            "checkerSha256": PINS[PREDECESSOR_CHECKER],
            "independentReview": PREDECESSOR_REVIEW,
            "independentReviewSha256": PINS[PREDECESSOR_REVIEW],
            "reviewVerdict": "PASS",
            "blockingFindingCount": 0,
            "applicationState": "CANDIDATE-NOT-APPLIED",
        },
        "whySuccessorAndNotInPlaceRepair": (
            "The v1.13 independent PASS binds the exact v1.13 bytes. Editing "
            "those bytes would silently invalidate the verdict that named "
            "them and would break the hashes other passed artifacts pin. "
            "v1.13, check-d9-v1.13.py and the v1.13 review therefore stay "
            "byte-untouched and are retained here as pinned repair input."
        ),
        "authorshipDisclosure": (
            "The v1.14 candidate and its checker share one author, and that "
            "author did not write the v1.13 independent review. The pinned "
            "v1.13 PASS is repair input, not approval of v1.14. A different "
            "agent must review the exact v1.14 bytes."
        ),
        "defectSource": (
            "A blind Consumer-B implementer litmus run against the passed "
            "v1.13 bytes. Both defects were independently verified before "
            "this successor was authored. Neither is a finding against the "
            "v1.13 review, which examined the predicates its checker states."
        ),
        "repairedDefects": [
            {
                "id": REPAIR_ONE_ID,
                "kind": "invalid value inside a closed vocabulary",
                "site": REPAIR_ONE_PATH,
                "v113Value": V113_REJECTION_VALUE,
                "v114Value": V114_REJECTION_VALUE,
                "closedEnum": "$.scenarioAxesSchema.properties.rejectionCause.enum",
                "finding": (
                    "The pre-reduction rejection cause of golden "
                    "fault-beats-rejection was invalid-config. The closed "
                    "rejectionCause enum contains config-invalid; "
                    "invalid-config is not a member of it and maps to no "
                    "entry of codeMaps.rejectionCauseToErrorCode."
                ),
                "deeperFinding": (
                    "check-d9-v1.13.py contains zero references to "
                    "rejectionCauses, and no checker in the retained chain "
                    "validates the cause values inside "
                    "concurrentConditionGoldens.conditions against the closed "
                    "axis enums. goldenCases axes are enum-checked; "
                    "pre-reduction condition records were not, so any "
                    "out-of-enum cause could sit there undetected. The value "
                    "fix is the symptom; D40-CAUSE-VALUE-CLOSURE is the repair."
                ),
                "behaviouralDelta": (
                    "None. faultCause precedes rejectionCause, so the reducer "
                    "drops the rejection family from the wire for this row. "
                    "The reduced family, cause and secondary list are "
                    "identical before and after the repair, which D42 proves "
                    "by running the retained reducer over both objects."
                ),
                "notRenamed": (
                    "goldenCases[15].id is the string "
                    "pre-admission-invalid-config. That is a golden NAME, not "
                    "an axis value, and it is deliberately unchanged."
                ),
                "enforcement": "check-d9-v1.14.py D40-CAUSE-VALUE-CLOSURE",
            },
            {
                "id": REPAIR_TWO_ID,
                "kind": "closed union field with no content disposition",
                "site": REPAIR_TWO_PATH,
                "v113Value": "{type: object, nullable: false}",
                "finding": (
                    "details was typed only as a non-null object. An "
                    "implementer could not know what may or must appear "
                    "inside it, whether it is closed, or whether anything in "
                    "it is actionable. Silence at a public union field is a "
                    "coherence defect even when no golden exercises the field."
                ),
                "repairChosen": (
                    "Explicit normative open-diagnostic-bag statement with no "
                    "semantic authority, not an invented closed schema."
                ),
                "whyThatRepair": (
                    "Zero goldens and zero retained core-completion rows carry "
                    "details, so there is no observed usage from which a "
                    "closed content schema could honestly be derived. A "
                    "guessed schema would add unreviewed semantics; removing "
                    "the field's authority adds none and is mechanically "
                    "checkable."
                ),
                "enforcement": "check-d9-v1.14.py D41-DETAILS-DISPOSITION",
            },
        ],
        "causeValueClosure": {
            "invariantId": "D9-V114-CAUSE-VALUE-CLOSURE",
            "rule": (
                "Every cause value that appears in any pre-reduction condition "
                "record anywhere in this contract MUST be a member of the "
                "corresponding closed scenario axis enum."
            ),
            "arrayToAxisEnum": {
                "faultCauses": "$.scenarioAxesSchema.properties.faultCause.enum",
                "rejectionCauses": "$.scenarioAxesSchema.properties.rejectionCause.enum",
                "deficiencies": "$.scenarioAxesSchema.properties.deficiency.enum",
                "secondaryDeficiencies": "$.scenarioAxesSchema.properties.secondaryDeficiencies.items.enum",
            },
            "shapeRule": (
                "A node is a pre-reduction condition record when at least one "
                "of the three plural primary names faultCauses, "
                "rejectionCauses or deficiencies is bound to a JSON array. "
                "Every such record MUST bind all three, and every present "
                "condition array MUST be an array of strings. The plural names "
                "are what separate a condition record from a reduced "
                "scenarioAxes record, which carries the singular axis names "
                "plus secondaryDeficiencies and is enum-checked as axes. The "
                "concurrentConditionReducer.inputSchema.properties node binds "
                "these names to type declarations rather than arrays and is "
                "therefore not a condition record."
            ),
            "sentinelRule": (
                "none means 'no cause in this family'. It is a legal reduced "
                "axis value and MUST NOT appear inside a pre-reduction "
                "condition array, where the empty array already means the same "
                "thing."
            ),
            "duplicateRule": "No duplicates within a single condition array.",
            "expectationRule": (
                "expectFamily and expectedFamily MUST be members of "
                "causeModel.families. expectCause and expectedCause MUST be "
                "members of the enum of the expected family. expectSecondaries "
                "and expectedSecondaries members MUST be members of the "
                "secondaryDeficiencies item enum."
            ),
            "scanRule": (
                "The closure is applied by recursive scan over the whole "
                "contract, not to a hard-coded pair of sites, so a future "
                "third condition record is covered without a checker change. "
                "The scan MUST also find every declared record: a mutation "
                "that deletes or retypes one is a finding."
            ),
            "declaredRecords": list(EXPECTED_CONDITION_RECORDS),
            "enforcement": "check-d9-v1.14.py D40-CAUSE-VALUE-CLOSURE",
            "mutationProof": (
                "--selftest restores invalid-config and requires a "
                "D40-CAUSE-VALUE-CLOSURE finding with the whole-object and "
                "raw-byte layers suppressed, so the repair is proved "
                "load-bearing on its own and not merely caught by successor "
                "equality."
            ),
        },
        "detailsFieldDisposition": {
            "invariantId": "D9-V114-DETAILS-NO-AUTHORITY",
            "site": REPAIR_TWO_PATH,
            "statementIsNormative": True,
            "teeth": [
                "details is optional on exactly one variant and required by none.",
                "details appears in zero goldenCases[*].expectedTermination.",
                "details appears in zero retainedCoreCompletionMatrix[*].expectedTermination.",
                "the reference derivation emits only reasonCodes or errorCode, never details.",
            ],
            "enforcement": "check-d9-v1.14.py D41-DETAILS-DISPOSITION",
            "mutationProof": (
                "--selftest restores the v1.13 two-key typing, weakens each "
                "normative key in turn, and plants details in a golden "
                "termination; every row must produce a "
                "D41-DETAILS-DISPOSITION finding with the whole-object and "
                "raw-byte layers suppressed."
            ),
        },
        "retainedSemanticsProof": {
            "invariantId": "D9-V114-GOLDEN-INVARIANCE",
            "rule": (
                "Every golden, retained core-completion row and pre-reduction "
                "record MUST derive the same class, ordered code payload and "
                "exit code under v1.14 as under pinned v1.13."
            ),
            "goldenCases": GOLDEN_COUNT,
            "retainedCoreCompletionRows": MATRIX_COUNT,
            "reductionRecords": REDUCTION_COUNT,
            "method": (
                "The retained pure derivation reached through the "
                "authenticated v1.13 closure is run twice, once over the v1.14 "
                "object and once over the pinned v1.13 object, and the two "
                "row sets must be equal. Each row must also equal its own "
                "declared expectedTermination and declared exit code."
            ),
            "enforcement": "check-d9-v1.14.py D42-GOLDEN-REDERIVATION",
        },
        "authorizedDelta": {
            "metadataKeys": list(AUTHORIZED_METADATA_KEYS),
            "addedKey": COMPATIBILITY_KEY,
            "semanticPaths": list(AUTHORIZED_SEMANTIC_DELTA_PATHS),
            "rule": (
                "Outside the listed successor-metadata keys and this added "
                "disposition, the ordered v1.14 object MUST differ from the "
                "ordered v1.13 object at exactly the two listed paths and "
                "nowhere else. D43-MINIMAL-SEMANTIC-DELTA computes the "
                "difference set and requires that exact equality."
            ),
            "enforcement": "check-d9-v1.14.py D43-MINIMAL-SEMANTIC-DELTA",
        },
        "representationCarryForward": {
            "v114ToV113Projection": (
                "Remove this disposition, restore the exact v1.13 successor "
                "metadata and trust fields, restore the v1.13 details typing "
                "and the v1.13 pre-reduction rejection cause; ordered object "
                "equality and canonical byte equality with pinned v1.13 are "
                "both required."
            ),
            "canonicalSerialization": (
                "json.dumps(obj, indent=2, ensure_ascii=True, "
                "sort_keys=False) + '\\n'"
            ),
            "protectedRawSource": (
                "Pinned v1.13 v111RepresentationDisposition.canonicalRawContract"
            ),
            "unchangedProtectedRoots": (
                "Every protected top-level raw root inherited from the v1.13 "
                "closure except hostTerminationUnion and "
                "concurrentConditionGoldens MUST remain byte-identical to "
                "v1.13. Those two MUST differ, and only by the two authorized "
                "repair paths."
            ),
            "requiredEscapedCodePoints": {"U+2014": 16, "U+2192": 1},
        },
        "semanticBoundary": (
            "No exit class, class-to-exit-code entry, code vocabulary, reason "
            "or error code, scenario axis enum, HostTermination union field "
            "set, variant, code map, cause model, precedence, reducer "
            "algorithm, golden expected termination, finalization transition, "
            "identity contract, remedy or frozen RT14 API change is permitted. "
            "The only functional deltas are the two declared repairs."
        ),
        "authorityBoundary": (
            "CANDIDATE-NOT-APPLIED / NO RT15, E8, OP6, product, TM, claim, "
            "narrative, integration, application or seal authority. A green "
            "authored checker is checker-scope evidence only."
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
    "A different agent who authored neither v1.14 nor its checker must verify "
    "stable hashes, the exact ordered and raw projections back to "
    "independently passed v1.13, that the semantic difference set is exactly "
    "the two declared repair paths, that the cause-value closure and the "
    "details disposition are each independently load-bearing under mutation, "
    "that all 45 goldens, 4 core-completion rows and 6 reduction records "
    "rederive identically, the complete frozen RT14 API, hostile-shape "
    "totality, and that --selftest genuinely executes its suite and refuses a "
    "dirty base with exit 3, before any application."
)
KNOWN_RESIDUAL = (
    "v1.14 is author-produced and not independently reviewed or applied. Its "
    "two repairs came from a blind Consumer-B implementer litmus over passed "
    "v1.13 bytes, which is evidence that authored review closure is "
    "incomplete, not that it is sound: a third coherence defect of the same "
    "class may still be present in a node no checker interrogates. The "
    "details repair removes authority rather than specifying content, so an "
    "implementer who needs structured rejection diagnostics still has no "
    "sanctioned place to put them and must raise that as a new requirement. "
    "No accepted RT15 exists and E8/OP6 remain unrejoined. Caller ownership "
    "of isolated startup is an explicit precondition. Checker greenness "
    "grants no product, integration, application or seal authority."
)


def _expected_successor(predecessor: dict[str, Any]) -> dict[str, Any]:
    expected = copy.deepcopy(predecessor)
    expected["version"] = EXPECTED_VERSION
    expected["status"] = EXPECTED_STATUS
    expected["supersedes"] = PREDECESSOR
    expected["purpose"] = EXPECTED_PURPOSE
    expected["checkerTrustOrderContract"] = _trust_contract()
    expected = _insert_after(expected, "v112StartupDisposition", [
        (COMPATIBILITY_KEY, _coherence_disposition()),
    ])
    expected["referenceDerivation"]["implementation"] = REFERENCE_IMPLEMENTATION
    expected["conformanceClaims"] = [{
        "claim": EXPECTED_CLAIM,
        "reproduce": NORMAL_COMMAND,
        "mutationProof": SELFTEST_COMMAND,
    }]
    expected["peerReviewRequired"][-1] = PEER_REVIEW
    expected["knownLimitations"][-1] = KNOWN_RESIDUAL
    # Repair 1: the only authorized pre-reduction cause-value change.
    expected["concurrentConditionGoldens"][0]["conditions"]["rejectionCauses"] = [
        V114_REJECTION_VALUE]
    # Repair 2: the only authorized HostTermination field-type change.
    expected["hostTerminationUnion"]["fieldTypes"][DETAILS_FIELD] = \
        copy.deepcopy(DETAILS_DISPOSITION)
    return expected


def _project_v113(candidate: dict[str, Any],
                  predecessor: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(candidate)
    projected.pop(COMPATIBILITY_KEY)
    for key in AUTHORIZED_METADATA_KEYS:
        projected[key] = copy.deepcopy(predecessor[key])
    projected["concurrentConditionGoldens"][0]["conditions"]["rejectionCauses"] = \
        copy.deepcopy(predecessor["concurrentConditionGoldens"][0][
            "conditions"]["rejectionCauses"])
    projected["hostTerminationUnion"]["fieldTypes"][DETAILS_FIELD] = \
        copy.deepcopy(predecessor["hostTerminationUnion"]["fieldTypes"][
            DETAILS_FIELD])
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


def _difference_paths(actual: Any, expected: Any, path: str,
                      out: list[str]) -> list[str]:
    if type(actual) is not type(expected):
        out.append(path)
        return out
    if isinstance(actual, dict):
        if list(actual) != list(expected):
            out.append(path)
            return out
        for key in expected:
            _difference_paths(actual[key], expected[key], f"{path}.{key}", out)
        return out
    if isinstance(actual, list):
        if len(actual) != len(expected):
            out.append(path)
            return out
        for index, (left, right) in enumerate(zip(actual, expected)):
            _difference_paths(left, right, f"{path}[{index}]", out)
        return out
    if actual != expected:
        out.append(path)
    return out


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(
        value, indent=2, ensure_ascii=True, sort_keys=False, allow_nan=False
    ) + "\n").encode("utf-8")


# ---------------------------------------------------------------------------
# D40: the closed pre-reduction cause-value closure (repair 1).
# ---------------------------------------------------------------------------
def _axis_enum(schema: Any, axis: str, from_items: bool) -> tuple[str, ...] | None:
    if not isinstance(schema, dict):
        return None
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return None
    node = properties.get(axis)
    if not isinstance(node, dict):
        return None
    if from_items:
        node = node.get("items")
        if not isinstance(node, dict):
            return None
    values = node.get("enum")
    if not isinstance(values, list) or not values or \
            any(not isinstance(item, str) for item in values):
        return None
    return tuple(values)


def _condition_records(node: Any, path: str, owner: Any,
                       out: list[tuple[str, dict[str, Any], Any]]) -> None:
    """Recursively collect every pre-reduction condition record and its owner."""
    if isinstance(node, dict):
        if any(isinstance(node.get(name), list)
               for name in PRIMARY_CONDITION_ARRAYS):
            out.append((path, node, owner))
        for key, value in node.items():
            if isinstance(key, str):
                _condition_records(value, f"{path}.{key}", node, out)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            _condition_records(value, f"{path}[{index}]", owner, out)


def _cause_closure_findings(candidate: dict[str, Any]) -> list[str]:
    prefix = "D40-CAUSE-VALUE-CLOSURE"
    findings: list[str] = []
    schema = candidate.get("scenarioAxesSchema")
    enums: dict[str, tuple[str, ...]] = {}
    for array_name, (axis, from_items) in CONDITION_ARRAYS.items():
        values = _axis_enum(schema, axis, from_items)
        if values is None:
            findings.append(
                f"{prefix}: closed enum for {array_name} is unreadable at "
                f"scenarioAxesSchema.properties.{axis}")
        else:
            enums[array_name] = values
    cause_model = candidate.get("causeModel")
    families = cause_model.get("families") if isinstance(cause_model, dict) else None
    if not isinstance(families, list) or not all(
            isinstance(item, str) for item in families):
        findings.append(f"{prefix}: causeModel.families is unreadable")
        families = []
    records: list[tuple[str, dict[str, Any], Any]] = []
    _condition_records(candidate, "$", None, records)
    found = tuple(path for path, _node, _owner in records)
    if sorted(found) != sorted(EXPECTED_CONDITION_RECORDS):
        findings.append(
            f"{prefix}: declared condition-record census drifted; found "
            f"{sorted(found)!r} != {sorted(EXPECTED_CONDITION_RECORDS)!r}")
    for path, node, owner in records:
        missing = [name for name in PRIMARY_CONDITION_ARRAYS
                   if not isinstance(node.get(name), list)]
        if missing:
            findings.append(
                f"{prefix}: {path} is a condition record but is missing the "
                f"required array(s) {missing!r}")
        for array_name in CONDITION_ARRAYS:
            if array_name not in node:
                continue
            values = node[array_name]
            if not isinstance(values, list):
                findings.append(
                    f"{prefix}: {path}.{array_name} is "
                    f"{type(values).__name__}, not an array")
                continue
            allowed = enums.get(array_name)
            seen: set[str] = set()
            for index, item in enumerate(values):
                where = f"{path}.{array_name}[{index}]"
                if not isinstance(item, str):
                    findings.append(
                        f"{prefix}: {where} is {type(item).__name__}, not a string")
                    continue
                if item == CAUSE_SENTINEL:
                    findings.append(
                        f"{prefix}: {where} is the sentinel {CAUSE_SENTINEL!r}; "
                        "an empty array is the only way to say 'no cause'")
                elif allowed is not None and item not in allowed:
                    findings.append(
                        f"{prefix}: {where}={item!r} is not a member of the "
                        f"closed {CONDITION_ARRAYS[array_name][0]} enum")
                if item in seen:
                    findings.append(f"{prefix}: {where}={item!r} is a duplicate")
                seen.add(item)
        if not isinstance(owner, dict):
            continue
        family = None
        for key in EXPECT_FAMILY_KEYS:
            if key in owner:
                family = owner[key]
                if not isinstance(family, str) or family not in families:
                    findings.append(
                        f"{prefix}: {path} owner {key}={family!r} is not a "
                        "declared cause family")
                    family = None
        for key in EXPECT_CAUSE_KEYS:
            if key not in owner:
                continue
            cause = owner[key]
            array_name = FAMILY_TO_ARRAY.get(family or "")
            allowed = enums.get(array_name or "")
            if not isinstance(cause, str):
                findings.append(
                    f"{prefix}: {path} owner {key} is {type(cause).__name__}, "
                    "not a string")
            elif allowed is not None and cause not in allowed:
                findings.append(
                    f"{prefix}: {path} owner {key}={cause!r} is not a member "
                    f"of the closed {family} enum")
        for key in EXPECT_SECONDARY_KEYS:
            if key not in owner:
                continue
            secondaries = owner[key]
            allowed = enums.get("secondaryDeficiencies")
            if not isinstance(secondaries, list):
                findings.append(
                    f"{prefix}: {path} owner {key} is "
                    f"{type(secondaries).__name__}, not an array")
                continue
            for index, item in enumerate(secondaries):
                if not isinstance(item, str) or (
                        allowed is not None and item not in allowed):
                    findings.append(
                        f"{prefix}: {path} owner {key}[{index}]={item!r} is "
                        "not a member of the closed secondaryDeficiencies enum")
    return findings


# ---------------------------------------------------------------------------
# D41: the HostTermination details disposition (repair 2).
# ---------------------------------------------------------------------------
def _details_findings(candidate: dict[str, Any]) -> list[str]:
    prefix = "D41-DETAILS-DISPOSITION"
    findings: list[str] = []
    union = candidate.get("hostTerminationUnion")
    if not isinstance(union, dict):
        return [f"{prefix}: hostTerminationUnion is not an object"]
    field_types = union.get("fieldTypes")
    if not isinstance(field_types, dict) or DETAILS_FIELD not in field_types:
        return [f"{prefix}: fieldTypes.{DETAILS_FIELD} is absent"]
    node = field_types[DETAILS_FIELD]
    if not isinstance(node, dict):
        return [f"{prefix}: fieldTypes.{DETAILS_FIELD} is not an object"]
    if node.get("type") != "object" or node.get("nullable") is not False:
        findings.append(
            f"{prefix}: the retained v1.13 typing of {DETAILS_FIELD} changed")
    if node.get("closed") is not False:
        findings.append(
            f"{prefix}: {DETAILS_FIELD} must declare closed=false; a closed "
            "content schema would assert semantics no golden exercises")
    if node.get("semanticAuthority") != "NONE":
        findings.append(
            f"{prefix}: {DETAILS_FIELD} must declare semanticAuthority=NONE")
    if node.get("controlFlowUse") != "FORBIDDEN":
        findings.append(
            f"{prefix}: {DETAILS_FIELD} must declare controlFlowUse=FORBIDDEN")
    rule = node.get("normativeRule")
    if not isinstance(rule, str) or not rule.strip():
        findings.append(f"{prefix}: {DETAILS_FIELD} carries no normativeRule")
    else:
        for token in DETAILS_REQUIRED_TOKENS:
            if token not in rule:
                findings.append(
                    f"{prefix}: normativeRule does not state {token!r}")
    for key in ("producerRules", "consumerRules"):
        rows = node.get(key)
        if not isinstance(rows, list) or not rows or any(
                not isinstance(row, str) or not row.strip() for row in rows):
            findings.append(
                f"{prefix}: {DETAILS_FIELD}.{key} must be a nonempty list of "
                "normative sentences")
    for key in ("declaredOn", "whyNotClosed", "derivationIndependence",
                "repairedIn"):
        value = node.get(key)
        if not isinstance(value, str) or not value.strip():
            findings.append(
                f"{prefix}: {DETAILS_FIELD}.{key} must be a nonempty statement")
    # Teeth: the statement is only true if nothing derives from the field.
    variants = union.get("variants")
    if not isinstance(variants, list):
        findings.append(f"{prefix}: hostTerminationUnion.variants is unreadable")
    else:
        required_on = [row.get("class") for row in variants
                       if isinstance(row, dict) and
                       DETAILS_FIELD in (row.get("required") or [])]
        optional_on = [row.get("class") for row in variants
                       if isinstance(row, dict) and
                       DETAILS_FIELD in (row.get("optional") or [])]
        if required_on:
            findings.append(
                f"{prefix}: {DETAILS_FIELD} is required by {required_on!r}; a "
                "field with no semantic authority may never be mandatory")
        if optional_on != ["request-rejected"]:
            findings.append(
                f"{prefix}: {DETAILS_FIELD} optional-variant set drifted to "
                f"{optional_on!r}")
    forbidden = union.get("forbiddenFields")
    if isinstance(forbidden, list) and DETAILS_FIELD in forbidden:
        findings.append(
            f"{prefix}: {DETAILS_FIELD} is both declared and forbidden")
    carriers: list[str] = []
    goldens = candidate.get("goldenCases")
    if isinstance(goldens, list):
        for index, row in enumerate(goldens):
            payload = row.get("expectedTermination") if isinstance(row, dict) else None
            if isinstance(payload, dict) and DETAILS_FIELD in payload:
                carriers.append(f"$.goldenCases[{index}].expectedTermination")
    contract = candidate.get("hostDerivedUnsatisfiableFinalizationContract")
    matrix = contract.get("retainedCoreCompletionMatrix") \
        if isinstance(contract, dict) else None
    if isinstance(matrix, list):
        for index, row in enumerate(matrix):
            payload = row.get("expectedTermination") if isinstance(row, dict) else None
            if isinstance(payload, dict) and DETAILS_FIELD in payload:
                carriers.append(
                    "$.hostDerivedUnsatisfiableFinalizationContract"
                    f".retainedCoreCompletionMatrix[{index}].expectedTermination")
    if carriers:
        findings.append(
            f"{prefix}: {len(carriers)} expected termination(s) carry "
            f"{DETAILS_FIELD}, so the no-authority statement is false; first "
            f"{carriers[0]}")
    return findings


# ---------------------------------------------------------------------------
# D42: every golden, matrix row and reduction record rederives identically.
# ---------------------------------------------------------------------------
def _payload_key(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False)


def _derived_rows(root: dict[str, Any]) -> list[tuple[str, ...]]:
    """The complete derived surface of one contract object, order preserved."""
    rows: list[tuple[str, ...]] = []
    maps = root["codeMaps"]
    exits = root["classToExitCode"]
    for golden in root["goldenCases"]:
        axes = copy.deepcopy(golden["scenarioAxes"])
        derived_class = derive_class(axes)
        codes = derive_codes(copy.deepcopy(axes), maps)
        rows.append((
            "golden", str(golden["id"]), derived_class, _payload_key(codes),
            _payload_key(exits[derived_class])))
    contract = root["hostDerivedUnsatisfiableFinalizationContract"]
    for row in contract["retainedCoreCompletionMatrix"]:
        axes = copy.deepcopy(row["axes"])
        derived_class = derive_class(axes)
        codes = derive_codes(copy.deepcopy(axes), maps)
        rows.append((
            "matrix", str(row["id"]), derived_class, _payload_key(codes),
            _payload_key(exits[derived_class])))
    precedence = list(root["causeModel"]["precedence"])
    for row in root["concurrentConditionGoldens"]:
        reduced = reduce_concurrent(copy.deepcopy(row["conditions"]), precedence)
        rows.append(("reduction", str(row["id"]), _payload_key(reduced), "", ""))
    control = contract["faultPrecedenceControl"]
    reduced = reduce_concurrent(copy.deepcopy(control["conditions"]), precedence)
    rows.append(("reduction", "faultPrecedenceControl",
                 _payload_key(reduced), "", ""))
    return rows


def _declared_rows(root: dict[str, Any]) -> list[tuple[str, ...]]:
    """The same surface as the contract itself declares it."""
    rows: list[tuple[str, ...]] = []
    exits = root["classToExitCode"]
    for golden in root["goldenCases"]:
        payload = golden["expectedTermination"]
        declared_class = payload["class"]
        codes = {key: payload[key] for key in ("reasonCodes", "errorCode")
                 if key in payload}
        rows.append((
            "golden", str(golden["id"]), declared_class, _payload_key(codes),
            _payload_key(exits[declared_class])))
    contract = root["hostDerivedUnsatisfiableFinalizationContract"]
    for row in contract["retainedCoreCompletionMatrix"]:
        payload = row["expectedTermination"]
        declared_class = payload["class"]
        codes = {key: payload[key] for key in ("reasonCodes", "errorCode")
                 if key in payload}
        rows.append((
            "matrix", str(row["id"]), declared_class, _payload_key(codes),
            _payload_key(row["expectedExitCode"])))
    for row in root["concurrentConditionGoldens"]:
        reduced = {"faultCause": "none", "rejectionCause": "none",
                   "deficiency": "none", "secondaryDeficiencies": []}
        reduced[row["expectFamily"]] = row["expectCause"]
        reduced["secondaryDeficiencies"] = list(row.get("expectSecondaries", []))
        rows.append(("reduction", str(row["id"]), _payload_key(reduced), "", ""))
    control = contract["faultPrecedenceControl"]
    reduced = {"faultCause": "none", "rejectionCause": "none",
               "deficiency": "none", "secondaryDeficiencies": []}
    reduced[control["expectedFamily"]] = control["expectedCause"]
    rows.append(("reduction", "faultPrecedenceControl",
                 _payload_key(reduced), "", ""))
    return rows


def _rederivation_findings(candidate: dict[str, Any],
                           predecessor: dict[str, Any]) -> list[str]:
    prefix = "D42-GOLDEN-REDERIVATION"
    findings: list[str] = []
    try:
        actual = _derived_rows(candidate)
        declared = _declared_rows(candidate)
        retained = _derived_rows(predecessor)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        return [f"{prefix}: rederivation raised {type(exc).__name__}: {exc}"]
    goldens = sum(1 for row in actual if row[0] == "golden")
    matrix = sum(1 for row in actual if row[0] == "matrix")
    reductions = sum(1 for row in actual if row[0] == "reduction")
    if (goldens, matrix, reductions) != (
            GOLDEN_COUNT, MATRIX_COUNT, REDUCTION_COUNT):
        findings.append(
            f"{prefix}: derived census {(goldens, matrix, reductions)} != "
            f"{(GOLDEN_COUNT, MATRIX_COUNT, REDUCTION_COUNT)}")
    if len(actual) != len(retained):
        findings.append(
            f"{prefix}: v1.14 derives {len(actual)} rows, pinned v1.13 "
            f"derives {len(retained)}")
    else:
        for left, right in zip(actual, retained):
            if left != right:
                findings.append(
                    f"{prefix}: {left[0]} {left[1]} does not rederive "
                    f"identically to pinned v1.13: {left[2:]!r} != {right[2:]!r}")
    if len(actual) != len(declared):
        findings.append(f"{prefix}: derived and declared row counts differ")
    else:
        for left, right in zip(actual, declared):
            if left != right:
                findings.append(
                    f"{prefix}: {left[0]} {left[1]} derives {left[2:]!r} but "
                    f"the contract declares {right[2:]!r}")
    return findings


# ---------------------------------------------------------------------------
# D43: the ordered semantic difference set is exactly the two repairs.
# ---------------------------------------------------------------------------
def _minimal_delta_findings(candidate: dict[str, Any],
                            predecessor: dict[str, Any]) -> list[str]:
    prefix = "D43-MINIMAL-SEMANTIC-DELTA"
    skip = set(AUTHORIZED_METADATA_KEYS) | {COMPATIBILITY_KEY}
    left = {key: value for key, value in candidate.items() if key not in skip}
    right = {key: value for key, value in predecessor.items() if key not in skip}
    paths: list[str] = []
    _difference_paths(left, right, "$", paths)
    if sorted(paths) != sorted(AUTHORIZED_SEMANTIC_DELTA_PATHS):
        return [
            f"{prefix}: semantic difference set {sorted(paths)!r} != the two "
            f"authorized repair paths {sorted(AUTHORIZED_SEMANTIC_DELTA_PATHS)!r}"
        ]
    return []


# ---------------------------------------------------------------------------
# Raw canonical preservation.
# ---------------------------------------------------------------------------
def _raw_findings(candidate_source: object, candidate: dict[str, Any],
                  expected: dict[str, Any], authority: Authority) -> list[str]:
    prefix = RAW_PREFIX
    if not isinstance(candidate_source, bytes):
        return [f"{prefix}: exact candidate source bytes are required"]
    findings: list[str] = []
    try:
        expected_source = _canonical_json(expected)
        actual_canonical = _canonical_json(candidate)
    except (TypeError, ValueError) as exc:
        return [f"{prefix}: cannot serialize candidate ({type(exc).__name__})"]
    if candidate_source != expected_source:
        findings.append(f"{prefix}: file differs from exact canonical v1.14")
    if candidate_source != actual_canonical:
        findings.append(f"{prefix}: file is not canonical serialization of its object")
    predecessor_source = authority.snapshots[PREDECESSOR]
    if _canonical_json(authority.predecessor) != predecessor_source:
        findings.append(f"{prefix}: pinned v1.13 canonical control failed")
    try:
        projected = _project_v113(candidate, authority.predecessor)
        if _canonical_json(projected) != predecessor_source:
            findings.append(f"{prefix}: canonical v1.13 projection is not exact")
        helpers = authority.helpers
        for key in helpers.PROTECTED_RAW_ROOTS:
            actual_span = helpers._top_level_raw_value(candidate_source, key)
            prior_span = helpers._top_level_raw_value(predecessor_source, key)
            if key in REPAIRED_RAW_ROOTS:
                if actual_span == prior_span:
                    findings.append(
                        f"{prefix}: repaired root {key} is unchanged from v1.13")
                if actual_span != helpers._top_level_raw_value(
                        expected_source, key):
                    findings.append(
                        f"{prefix}: repaired root {key} is not the exact "
                        "authorized span")
            elif actual_span != prior_span:
                findings.append(f"{prefix}: protected root {key} drifted")
        for key, indexes in helpers.PROTECTED_ARRAY_PREFIXES.items():
            actual_rows = helpers._array_raw_elements(
                helpers._top_level_raw_value(candidate_source, key))
            prior_rows = helpers._array_raw_elements(
                helpers._top_level_raw_value(predecessor_source, key))
            for index in indexes:
                if actual_rows[index] != prior_rows[index]:
                    findings.append(
                        f"{prefix}: protected element {key}[{index}] drifted")
    except (AttributeError, IndexError, KeyError, TypeError, ValueError,
            UnicodeError, json.JSONDecodeError) as exc:
        findings.append(f"{prefix}: raw projection raised {type(exc).__name__}")
    if candidate_source.count(b"\\u2014") != 16 or \
            candidate_source.count(b"\\u2192") != 1 or \
            b"\xe2\x80\x94" in candidate_source or \
            b"\xe2\x86\x92" in candidate_source:
        findings.append(f"{prefix}: inherited lexical diagnostics drifted")
    return findings


def _public_api_view() -> types.ModuleType:
    module = types.ModuleType("opensip_d9_v114_public_api_view")
    module.check = check
    module.derive_class = derive_class
    module.derive_codes = derive_codes
    module.reduce_concurrent = reduce_concurrent
    module.V17 = V17
    return module


# ---------------------------------------------------------------------------
# Source-level guards: startup order and live --selftest reachability.
# ---------------------------------------------------------------------------
def _startup_source_findings(source: bytes) -> list[str]:
    findings: list[str] = []
    try:
        tree = ast.parse(source.decode("utf-8"), filename=CHECKER)
    except (UnicodeError, SyntaxError, ValueError) as exc:
        return [f"D37R-STARTUP-SOURCE: cannot parse checker ({type(exc).__name__})"]
    body = tree.body
    imports = [node for node in body if isinstance(node, (ast.Import, ast.ImportFrom))]
    sys_import = next((node for node in imports if isinstance(node, ast.Import)
                       and [alias.name for alias in node.names] == ["sys"]), None)
    guard = next((node for node in body if isinstance(node, ast.If)
                  and ast.unparse(node.test) == "sys.flags.isolated != 1"), None)
    if sys_import is None or guard is None:
        return ["D37R-STARTUP-SOURCE: exact sys import/isolated guard absent"]
    intervening = [node for node in imports
                   if sys_import.lineno < node.lineno < guard.lineno]
    if intervening:
        findings.append("D37R-STARTUP-SOURCE: import occurs before isolated guard")
    later_imports = [node for node in imports if node is not sys_import and
                     not (isinstance(node, ast.ImportFrom) and
                          node.module == "__future__")]
    if any(node.lineno < guard.lineno for node in later_imports):
        findings.append("D37R-STARTUP-SOURCE: non-sys import precedes guard")
    has_refusal = any(isinstance(node, ast.Call) and
                      isinstance(node.func, ast.Name) and node.func.id == "print"
                      for node in ast.walk(guard))
    has_exit = any(isinstance(node, ast.Raise) and
                   "SystemExit(2)" in ast.unparse(node)
                   for node in ast.walk(guard))
    if not has_refusal or not has_exit:
        findings.append("D37R-STARTUP-SOURCE: guard lacks exact refusal/exit")
    bootstrap_line = next((node.lineno for node in body if isinstance(node, ast.Assign)
                           and any(isinstance(target, ast.Name) and
                                   target.id == "_BOOTSTRAP_AUTHORITY"
                                   for target in node.targets)), None)
    if bootstrap_line is None or bootstrap_line <= guard.lineno:
        findings.append("D37R-STARTUP-SOURCE: bootstrap is not after guard")
    return findings


def _selftest_reachability_findings(source: bytes) -> list[str]:
    """The evidence.v8 defect: --selftest that never reaches its own suite."""
    prefix = "D44-SELFTEST-REACHABILITY"
    try:
        tree = ast.parse(source.decode("utf-8"), filename=CHECKER)
    except (UnicodeError, SyntaxError, ValueError) as exc:
        return [f"{prefix}: cannot parse this checker ({type(exc).__name__})"]
    findings: list[str] = []
    mains = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "main"]
    if len(mains) != 1:
        return [f"{prefix}: this checker does not define exactly one main()"]
    selftest_index: int | None = None
    findings_return_index: int | None = None
    for index, statement in enumerate(mains[0].body):
        text = ast.dump(statement)
        if selftest_index is None and "'--selftest'" in text and \
                "Name(id='selftest'" in text:
            selftest_index = index
        if findings_return_index is None and "Name(id='findings'" in text and \
                "Return(" in text:
            findings_return_index = index
    if selftest_index is None:
        findings.append(f"{prefix}: main() never dispatches to selftest()")
    elif findings_return_index is not None and \
            findings_return_index < selftest_index:
        findings.append(
            f"{prefix}: main() can return on findings before the selftest suite")
    suites = [node for node in tree.body
              if isinstance(node, ast.FunctionDef) and node.name == "selftest"]
    if len(suites) != 1:
        findings.append(f"{prefix}: this checker does not define one selftest()")
    else:
        iterated = {node.iter.id for node in ast.walk(suites[0])
                    if isinstance(node, ast.For) and isinstance(node.iter, ast.Name)}
        for suite in ("REPAIR_MUTATIONS", "OBJECT_MUTATIONS"):
            if suite not in iterated:
                findings.append(
                    f"{prefix}: selftest() never iterates {suite}")
        returns_three = any(
            isinstance(node, ast.Return) and isinstance(node.value, ast.Constant)
            and node.value.value == 3 for node in ast.walk(suites[0]))
        if not returns_three:
            findings.append(
                f"{prefix}: selftest() has no distinct exit-3 dirty-base refusal")
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in {
                "TODO_FINDINGS", "TODO_DECLARATIONS"}:
            findings.append(f"{prefix}: this checker carries a TODO findings gate")
            break
    return findings


# ---------------------------------------------------------------------------
# The complete contract check.
# ---------------------------------------------------------------------------
def _check_contract(candidate: object, authority: Authority,
                    candidate_source: object = None) -> list[str]:
    if not isinstance(candidate, dict) or not candidate:
        return ["D9V114-TOTALITY-ROOT: v1.14 candidate must be a nonempty object"]
    findings: list[str] = []
    try:
        expected = _expected_successor(authority.predecessor)
        try:
            projected = _project_v113(candidate, authority.predecessor)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
            findings.append(
                f"D38R-PROJECTION: cannot project to v1.13 ({type(exc).__name__})")
            projected = None
        if projected is not None:
            difference = _first_difference(projected, authority.predecessor)
            if difference:
                findings.append(
                    f"D38R-PROJECTION: v1.14 is not exact v1.13; {difference}")
            retained = authority.v113_checker._check_contract(
                projected, authority.v113_authority, _canonical_json(projected))
            findings.extend(
                f"v1.13 retained checker: {item}" for item in retained)
        difference = _first_difference(candidate, expected)
        if difference:
            findings.append(f"D39R-EXACT-DELTA: unauthorized delta; {difference}")
        findings.extend(_minimal_delta_findings(candidate, authority.predecessor))
        findings.extend(_cause_closure_findings(candidate))
        findings.extend(_details_findings(candidate))
        findings.extend(_rederivation_findings(candidate, authority.predecessor))
        if (sys.flags.isolated, sys.flags.ignore_environment,
                sys.flags.no_user_site) != (1, 1, 1):
            findings.append(
                "D37R-STARTUP-FLAGS: isolated/ignore_environment/no_user_site "
                "must all equal 1")
        checker_source = (HERE / CHECKER).read_bytes()
        findings.extend(_startup_source_findings(checker_source))
        findings.extend(_selftest_reachability_findings(checker_source))
        surface = authority.predecessor["v111RepresentationDisposition"][
            "retainedRuntimeSurface"]
        public = _public_api_view()
        helpers = authority.helpers
        findings.extend(helpers._surface_resolution_findings(public, surface))
        findings.extend(helpers._runtime_invocation_findings(
            public, authority.v112_authority))
        findings.extend(_raw_findings(
            candidate_source, candidate, expected, authority))
    except (AttributeError, IndexError, KeyError, StopIteration, TypeError,
            ValueError, OSError) as exc:
        findings.append(
            f"D9V114-TOTALITY-EXCEPTION: malformed parsed shape "
            f"({type(exc).__name__})")
    return findings


# ---------------------------------------------------------------------------
# Mutation suites.
# ---------------------------------------------------------------------------
def _disposition(root: dict[str, Any]) -> dict[str, Any]:
    value = root[COMPATIBILITY_KEY]
    if not isinstance(value, dict):
        raise TypeError(COMPATIBILITY_KEY)
    return value


def _details_node(root: dict[str, Any]) -> dict[str, Any]:
    value = root["hostTerminationUnion"]["fieldTypes"][DETAILS_FIELD]
    if not isinstance(value, dict):
        raise TypeError(DETAILS_FIELD)
    return value


def _conditions(root: dict[str, Any], index: int) -> dict[str, Any]:
    value = root["concurrentConditionGoldens"][index]["conditions"]
    if not isinstance(value, dict):
        raise TypeError("conditions")
    return value


Mutation = tuple[str, Callable[[dict[str, Any]], None]]

# Rows whose only required rejecter is the named repair check, proved with the
# whole-object and raw-byte layers suppressed.
RepairMutation = tuple[str, str, Callable[[dict[str, Any]], None]]
REPAIR_MUTATIONS: list[RepairMutation] = [
    ("restore the v1.13 invalid-config value", "D40-CAUSE-VALUE-CLOSURE",
     lambda root: _conditions(root, 0).__setitem__(
         "rejectionCauses", [V113_REJECTION_VALUE])),
    ("out-of-enum faultCause", "D40-CAUSE-VALUE-CLOSURE",
     lambda root: _conditions(root, 1).__setitem__(
         "faultCauses", ["cas-broken-link"])),
    ("out-of-enum deficiency", "D40-CAUSE-VALUE-CLOSURE",
     lambda root: _conditions(root, 2).__setitem__(
         "deficiencies", ["relation-required-missing"])),
    ("out-of-enum secondary deficiency", "D40-CAUSE-VALUE-CLOSURE",
     lambda root: _conditions(root, 3).__setitem__(
         "secondaryDeficiencies", ["budget-blown"])),
    ("sentinel none inside a condition array", "D40-CAUSE-VALUE-CLOSURE",
     lambda root: _conditions(root, 2).__setitem__(
         "rejectionCauses", ["unsatisfiable", CAUSE_SENTINEL])),
    ("duplicate cause inside a condition array", "D40-CAUSE-VALUE-CLOSURE",
     lambda root: _conditions(root, 3).__setitem__(
         "deficiencies", ["provider-unavailable", "budget-exhausted",
                          "budget-exhausted"])),
    ("condition array retyped to a string", "D40-CAUSE-VALUE-CLOSURE",
     lambda root: _conditions(root, 0).__setitem__(
         "rejectionCauses", V114_REJECTION_VALUE)),
    ("condition array carries a non-string", "D40-CAUSE-VALUE-CLOSURE",
     lambda root: _conditions(root, 4).__setitem__("faultCauses", [7])),
    ("delete a declared condition record", "D40-CAUSE-VALUE-CLOSURE",
     lambda root: root["concurrentConditionGoldens"][4].pop("conditions")),
    ("out-of-enum expectCause", "D40-CAUSE-VALUE-CLOSURE",
     lambda root: root["concurrentConditionGoldens"][2].__setitem__(
         "expectCause", "not-satisfiable")),
    ("out-of-enum matrix control cause", "D40-CAUSE-VALUE-CLOSURE",
     lambda root: root["hostDerivedUnsatisfiableFinalizationContract"][
         "faultPrecedenceControl"]["conditions"].__setitem__(
             "rejectionCauses", ["invalid-config"])),
    ("restore the v1.13 contentless details typing", "D41-DETAILS-DISPOSITION",
     lambda root: root["hostTerminationUnion"]["fieldTypes"].__setitem__(
         DETAILS_FIELD, {"type": "object", "nullable": False})),
    ("details claims semantic authority", "D41-DETAILS-DISPOSITION",
     lambda root: _details_node(root).__setitem__(
         "semanticAuthority", "AUTHORITATIVE")),
    ("details claims a closed schema", "D41-DETAILS-DISPOSITION",
     lambda root: _details_node(root).__setitem__("closed", True)),
    ("details permits control flow", "D41-DETAILS-DISPOSITION",
     lambda root: _details_node(root).__setitem__("controlFlowUse", "PERMITTED")),
    ("details normative rule loses its prohibition", "D41-DETAILS-DISPOSITION",
     lambda root: _details_node(root).__setitem__(
         "normativeRule", "details is an object.")),
    ("details drops its normative rule", "D41-DETAILS-DISPOSITION",
     lambda root: _details_node(root).pop("normativeRule")),
    ("details drops its producer rules", "D41-DETAILS-DISPOSITION",
     lambda root: _details_node(root).__setitem__("producerRules", [])),
    ("details drops whyNotClosed", "D41-DETAILS-DISPOSITION",
     lambda root: _details_node(root).pop("whyNotClosed")),
    ("details becomes required on a variant", "D41-DETAILS-DISPOSITION",
     lambda root: root["hostTerminationUnion"]["variants"][2]["required"].append(
         DETAILS_FIELD)),
    ("details spreads to a second variant", "D41-DETAILS-DISPOSITION",
     lambda root: root["hostTerminationUnion"]["variants"][4]["optional"].append(
         DETAILS_FIELD)),
    ("a golden termination starts carrying details", "D41-DETAILS-DISPOSITION",
     lambda root: root["goldenCases"][15]["expectedTermination"].__setitem__(
         DETAILS_FIELD, {"hint": "config"})),
    ("a matrix row starts carrying details", "D41-DETAILS-DISPOSITION",
     lambda root: root["hostDerivedUnsatisfiableFinalizationContract"][
         "retainedCoreCompletionMatrix"][0]["expectedTermination"].__setitem__(
             DETAILS_FIELD, {"hint": "unsatisfiable"})),
    ("a golden expected class flips", "D42-GOLDEN-REDERIVATION",
     lambda root: root["goldenCases"][0]["expectedTermination"].__setitem__(
         "class", "indeterminate")),
    ("a golden error code flips", "D42-GOLDEN-REDERIVATION",
     lambda root: root["goldenCases"][15]["expectedTermination"].__setitem__(
         "errorCode", "IDENTITY.UNKNOWN")),
    ("a class exit code drifts", "D42-GOLDEN-REDERIVATION",
     lambda root: root["classToExitCode"].__setitem__("indeterminate", 9)),
    ("a used code map entry drifts", "D42-GOLDEN-REDERIVATION",
     lambda root: root["codeMaps"]["rejectionCauseToErrorCode"].__setitem__(
         "config-invalid", "CONFIG.BROKEN")),
    ("the reducer precedence reverses", "D42-GOLDEN-REDERIVATION",
     lambda root: root["causeModel"].__setitem__(
         "precedence", list(reversed(root["causeModel"]["precedence"])))),
    ("a matrix expected exit code drifts", "D42-GOLDEN-REDERIVATION",
     lambda root: root["hostDerivedUnsatisfiableFinalizationContract"][
         "retainedCoreCompletionMatrix"][1].__setitem__("expectedExitCode", 5)),
    ("an unauthorized semantic edit outside the repairs",
     "D43-MINIMAL-SEMANTIC-DELTA",
     lambda root: root["hostTerminationUnion"].__setitem__(
         "unknownFieldPolicy", "ignore")),
]

OBJECT_MUTATIONS: list[Mutation] = [
    ("version", lambda root: root.__setitem__("version", "v1.13")),
    ("status promotion", lambda root: root.__setitem__("status", "APPLIED")),
    ("wrong supersedes", lambda root: root.__setitem__("supersedes", V112)),
    ("drop v1.13 disposition", lambda root: root.pop(COMPATIBILITY_KEY)),
    ("downgrade the v1.13 verdict", lambda root: _disposition(root)[
        "passedPredecessor"].__setitem__("reviewVerdict", "REJECT")),
    ("hide a v1.13 blocker", lambda root: _disposition(root)[
        "passedPredecessor"].__setitem__("blockingFindingCount", 1)),
    ("wrong v1.13 artifact pin", lambda root: _disposition(root)[
        "passedPredecessor"].__setitem__("artifactSha256", "0" * 64)),
    ("wrong v1.13 checker pin", lambda root: _disposition(root)[
        "passedPredecessor"].__setitem__("checkerSha256", "0" * 64)),
    ("wrong v1.13 review pin", lambda root: _disposition(root)[
        "passedPredecessor"].__setitem__("independentReviewSha256", "0" * 64)),
    ("claim independent approval", lambda root: _disposition(root).__setitem__(
        "authorshipDisclosure", "independently reviewed and approved")),
    ("drop a repaired defect record", lambda root: _disposition(root)[
        "repairedDefects"].pop()),
    ("rename the repair-one site", lambda root: _disposition(root)[
        "repairedDefects"][0].__setitem__("site", "$.goldenCases[15].id")),
    ("deny the closure gap", lambda root: _disposition(root)[
        "repairedDefects"][0].__setitem__(
            "deeperFinding", "the retained chain already validated this")),
    ("weaken the closure scan rule", lambda root: _disposition(root)[
        "causeValueClosure"].__setitem__(
            "scanRule", "check the first golden only")),
    ("drop a declared condition record", lambda root: _disposition(root)[
        "causeValueClosure"]["declaredRecords"].pop()),
    ("weaken the details teeth", lambda root: _disposition(root)[
        "detailsFieldDisposition"]["teeth"].pop()),
    ("deny that the details statement is normative",
     lambda root: _disposition(root)["detailsFieldDisposition"].__setitem__(
         "statementIsNormative", False)),
    ("understate the golden count", lambda root: _disposition(root)[
        "retainedSemanticsProof"].__setitem__("goldenCases", 44)),
    ("widen the authorized delta", lambda root: _disposition(root)[
        "authorizedDelta"]["semanticPaths"].append("$.classToExitCode")),
    ("erase the semantic boundary", lambda root: _disposition(root).__setitem__(
        "semanticBoundary", "any change is permitted")),
    ("promote the authority boundary", lambda root: _disposition(root).__setitem__(
        "authorityBoundary", "APPLIED with seal authority")),
    ("normal command drops -I", lambda root: root["checkerTrustOrderContract"][
        "startupTrustRoot"].__setitem__(
            "normalCommand", "python3 -B artifacts/check-d9-v1.14.py")),
    ("script owns trust", lambda root: root["checkerTrustOrderContract"][
        "startupTrustRoot"].__setitem__("owner", "script")),
    ("remove early refusal", lambda root: root["checkerTrustOrderContract"][
        "startupTrustRoot"].pop("earlyRefusal")),
    ("collapse exit 3 onto exit 1", lambda root: root[
        "checkerTrustOrderContract"]["exitCodes"].pop("3")),
    ("child drops -I", lambda root: root["checkerTrustOrderContract"][
        "childProcessRule"].__setitem__(
            "authorityBearingPrefix", ["sys.executable", "-B"])),
    ("negative control grants authority", lambda root: root[
        "checkerTrustOrderContract"]["childProcessRule"][
            "negativeControlException"].__setitem__("authority", "PASS")),
    ("drop trust input", lambda root: root["checkerTrustOrderContract"][
        "transitiveInputs"].pop()),
    ("reverse trust order", lambda root: root["checkerTrustOrderContract"][
        "requiredOrder"].reverse()),
    ("old reference", lambda root: root["referenceDerivation"].__setitem__(
        "implementation", "artifacts/check-d9-v1.13.py")),
    ("conformance drops -I", lambda root: root["conformanceClaims"][0].__setitem__(
        "reproduce", "python3 -B artifacts/check-d9-v1.14.py")),
    ("drop peer review", lambda root: root["peerReviewRequired"].pop()),
    ("drop residual", lambda root: root["knownLimitations"].pop()),
    ("semantic exit drift", lambda root: root["classToExitCode"].__setitem__(
        "success", 99)),
    ("rename the invalid-config golden", lambda root: root["goldenCases"][
        15].__setitem__("id", "pre-admission-config-invalid")),
]


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
HOSTILE_KEYS = (
    "checkerTrustOrderContract", "v111RepresentationDisposition",
    "v112StartupDisposition", COMPATIBILITY_KEY, "exitClasses",
    "referenceDerivation", "conformanceClaims", "goldenCases",
    "peerReviewRequired", "knownLimitations", "scenarioAxesSchema",
    "classToExitCode", "codeMaps", "causeModel", "crossAxisInvariants",
    "concurrentConditionReducer", "concurrentConditionGoldens",
    "hostTerminationUnion", "hostDerivedUnsatisfiableFinalizationContract",
)
HOSTILE_NESTED = (
    ("hostTerminationUnion", "fieldTypes"),
    ("hostTerminationUnion", "variants"),
    ("scenarioAxesSchema", "properties"),
    ("causeModel", "families"),
    ("causeModel", "precedence"),
    ("codeMaps", "rejectionCauseToErrorCode"),
    ("hostDerivedUnsatisfiableFinalizationContract",
     "retainedCoreCompletionMatrix"),
    ("hostDerivedUnsatisfiableFinalizationContract", "faultPrecedenceControl"),
)


def _hostile_candidates(candidate: dict[str, Any]) -> list[tuple[str, Any]]:
    rows = list(HOSTILE_ROOTS)
    for key in HOSTILE_KEYS:
        for value in (None, "hostile", [], 0):
            changed = copy.deepcopy(candidate)
            changed[key] = value
            rows.append((f"{key}={value!r}", changed))
    for outer, inner in HOSTILE_NESTED:
        for value in (None, "hostile", []):
            changed = copy.deepcopy(candidate)
            changed[outer][inner] = value
            rows.append((f"{outer}.{inner}={value!r}", changed))
    for index in (0, 4):
        for value in (None, "hostile", [], {}):
            changed = copy.deepcopy(candidate)
            changed["concurrentConditionGoldens"][index]["conditions"] = value
            rows.append((f"conditions[{index}]={value!r}", changed))
    for value in (None, "hostile", [], 0):
        changed = copy.deepcopy(candidate)
        changed["hostTerminationUnion"]["fieldTypes"][DETAILS_FIELD] = value
        rows.append((f"details={value!r}", changed))
        changed = copy.deepcopy(candidate)
        changed["goldenCases"][0]["scenarioAxes"] = value
        rows.append((f"goldenCases[0].scenarioAxes={value!r}", changed))
        changed = copy.deepcopy(candidate)
        changed["goldenCases"][0]["expectedTermination"] = value
        rows.append((f"goldenCases[0].expectedTermination={value!r}", changed))
    return rows


# ---------------------------------------------------------------------------
# Child-process controls.
# ---------------------------------------------------------------------------
_ORIGINAL_SUBPROCESS_RUN = subprocess.run


def _sanitized_env(base: Mapping[str, str] | None = None) -> dict[str, str]:
    source = dict(os.environ if base is None else base)
    return {key: value for key, value in source.items()
            if not key.upper().startswith(PYTHON_ENV_PREFIX)}


def _retained_v113_selftest(candidate: dict[str, Any], authority: Authority
                            ) -> tuple[int, list[dict[str, Any]]]:
    """Run the authenticated v1.13 suite over the projection, observing children.

    The observer records and validates; it never rewrites argv.  Rewriting
    would destroy the reviewed v1.13 negative control, which deliberately
    launches a nonisolated child and requires the exact refusal.
    """
    child_log: list[dict[str, Any]] = []
    module = authority.v113_checker
    retained_original = module._ORIGINAL_SUBPROCESS_RUN

    def observer(command: Any, *args: Any, **kwargs: Any) -> Any:
        if not isinstance(command, (list, tuple)) or not command or \
                os.fspath(command[0]) != sys.executable:
            raise RuntimeError("retained harness attempted a non-Python child")
        argv = [os.fspath(item) for item in command]
        environment = kwargs.get("env")
        keys = sorted(key for key in (environment or {})
                      if key.upper().startswith(PYTHON_ENV_PREFIX))
        child_log.append({
            "argv": argv[:3],
            "isolated": argv[1:3] == ["-I", "-B"],
            "pythonEnvironmentKeys": keys,
            "shell": bool(kwargs.get("shell")),
            "explicitEnv": environment is not None,
        })
        return retained_original(command, *args, **kwargs)

    module._ORIGINAL_SUBPROCESS_RUN = observer
    try:
        projected = _project_v113(candidate, authority.predecessor)
        result = module.selftest(
            projected, authority.snapshots[PREDECESSOR],
            authority.v113_authority, module.DeferredAuthorityLoader())
    finally:
        module._ORIGINAL_SUBPROCESS_RUN = retained_original
    return result, child_log


def _child_census_findings(rows: list[dict[str, Any]]) -> list[str]:
    findings: list[str] = []
    if not rows:
        findings.append("no retained child was observed")
        return findings
    if any(row["shell"] for row in rows):
        findings.append("a retained child used shell=True")
    if any(not row["explicitEnv"] for row in rows):
        findings.append("a retained child inherited the ambient environment")
    nonisolated = [row for row in rows if not row["isolated"]]
    if len(nonisolated) != 1:
        findings.append(
            f"{len(nonisolated)} nonisolated children; exactly one documented "
            "negative control is admitted")
    if any(row["pythonEnvironmentKeys"] for row in nonisolated):
        findings.append("the negative control carried a PYTHON* entry")
    isolated = [row for row in rows if row["isolated"]]
    marked = [row for row in isolated if row["pythonEnvironmentKeys"]]
    if len(marked) != 1 or marked[0]["pythonEnvironmentKeys"] != ["PYTHONPATH"]:
        findings.append(
            f"{len(marked)} isolated children carried PYTHON* entries; exactly "
            "one documented PYTHONPATH marker control is admitted")
    return findings


def _clean_nonisolated_refusal() -> tuple[bool, str]:
    # Copy only the checker: the exact refusal must not need or read any pin.
    with tempfile.TemporaryDirectory(prefix="opensip-d9-v114-refusal-") as raw:
        directory = pathlib.Path(raw)
        isolated_checker = directory / CHECKER
        shutil.copy2(HERE / CHECKER, isolated_checker)
        command = [sys.executable, "-B", str(isolated_checker)]
        completed = _ORIGINAL_SUBPROCESS_RUN(
            command, cwd=directory, env=_sanitized_env(), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=60, check=False)
        exact = completed.stdout == "" and \
            completed.stderr == STARTUP_REFUSAL + "\n"
        return completed.returncode == 2 and exact, \
            f"rc={completed.returncode}, exact={exact}, pins-present=False"


def _isolated_environment_control() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="opensip-d9-v114-start-") as raw:
        directory = pathlib.Path(raw)
        marker = directory / "startup-marker"
        sitecustomize = directory / "sitecustomize.py"
        sitecustomize.write_text(
            "from pathlib import Path\n"
            f"Path({str(marker)!r}).write_text('LOCAL-MARKER')\n")
        environment = _sanitized_env()
        # Deliberately present only for this -I control. The isolated
        # interpreter must ignore it.
        environment["PYTHONPATH"] = str(directory)
        completed = _ORIGINAL_SUBPROCESS_RUN(
            [sys.executable, "-I", "-B", str(HERE / CHECKER)],
            cwd=HERE, env=environment, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=60, check=False)
        passed = completed.returncode == 0 and not marker.exists() and \
            "D9 v1.14 contract OK" in completed.stdout
        return passed, f"rc={completed.returncode}, marker={marker.exists()}"


def _dirty_base_exit_control() -> tuple[bool, str]:
    """--selftest over a dirty base must exit 3, not 0, 1 or 2."""
    with tempfile.TemporaryDirectory(prefix="opensip-d9-v114-dirty-") as raw:
        directory = pathlib.Path(raw) / "artifacts"
        directory.mkdir(parents=True)
        for source in HERE.iterdir():
            if source.is_file():
                shutil.copy2(source, directory / source.name)
        dirty = directory / "d9-exit-contract.v1.14-dirty.json"
        dirty.write_bytes(
            (HERE / BINDING).read_bytes().replace(b"{\n", b"{ \n", 1))
        completed = _ORIGINAL_SUBPROCESS_RUN(
            [sys.executable, "-I", "-B", str(directory / CHECKER),
             str(dirty), "--selftest"],
            cwd=directory, env=_sanitized_env(), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=120, check=False)
        passed = completed.returncode == 3 and \
            "SELFTEST-REFUSED" in completed.stdout and \
            "SELFTEST-NOT-RUN" in completed.stdout
        return passed, f"rc={completed.returncode} (must be 3)"


def _rt14_rebind_probe() -> tuple[bool, str, list[dict[str, Any]]]:
    checker_digest = hashlib.sha256((HERE / CHECKER).read_bytes()).hexdigest()
    child_log: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="opensip-d9-v114-rt14-") as raw:
        directory = pathlib.Path(raw) / "artifacts"
        directory.mkdir(parents=True)
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
        rebound_checker = directory / "check-retention-custody-v14-d9-v114-sim.py"
        rebound_checker.write_text(rebound)
        candidate = json.loads((directory / RT14).read_text())
        row = candidate["contextualD9Rejoin"]["authority"]
        row["d9Checker"] = CHECKER
        row["d9CheckerSha256"] = checker_digest
        rebound_candidate = directory / "retention-tiers.v14-d9-v114-sim.json"
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
                    if key.upper().startswith(PYTHON_ENV_PREFIX)),
            })
            completed = _ORIGINAL_SUBPROCESS_RUN(
                command, cwd=directory, env=environment, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                timeout=300, check=False)
            if completed.returncode != 0:
                tail = "\n".join(completed.stdout.splitlines()[-12:])
                return (False,
                        f"RT14 {'selftest' if extra else 'normal'} failed: {tail}",
                        child_log)
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


# ---------------------------------------------------------------------------
# The live self-test.
# ---------------------------------------------------------------------------
def selftest(candidate: Any, candidate_source: Any, authority: Authority,
             loader: DeferredAuthorityLoader) -> int:
    """Always reaches the suites; refuses a dirty base with a distinct code 3."""
    if not isinstance(candidate, dict) or not isinstance(candidate_source, bytes):
        print("SELFTEST-REFUSED: selftest requires an object root and exact bytes")
        print("SELFTEST-NOT-RUN: 0 mutations executed; exit 3 distinguishes "
              "this refusal from a green selftest and from ordinary findings.")
        return 3
    base = _check_contract(candidate, authority, candidate_source)
    if base:
        print("SELFTEST-REFUSED: the base candidate is not clean, so the "
              "mutation suite is not an oracle over it.")
        print(f"  dirty base: {len(base)} finding(s) in the candidate")
        for finding in base[:10]:
            print("  base-finding:", finding)
        if len(base) > 10:
            print(f"  ... {len(base) - 10} further base finding(s)")
        print(f"SELFTEST-NOT-RUN: 0 of "
              f"{len(REPAIR_MUTATIONS) + len(OBJECT_MUTATIONS)} mutations "
              "executed; exit 3 distinguishes this refusal from a green "
              "selftest, from ordinary findings and from a bad invocation.")
        return 3

    print("D9 v1.14 live self-test")
    print(f"  base: {len(candidate_source)} canonical bytes, 0 findings")
    startup_flags = (sys.flags.isolated, sys.flags.ignore_environment,
                     sys.flags.no_user_site) == (1, 1, 1)
    print(f"  {'pass' if startup_flags else 'FAIL':>6}  "
          "isolated/ignore_environment/no_user_site flags are all 1")

    print("\nrepair mutations - each row must be rejected by its own repair "
          "check with the whole-object and raw-byte layers suppressed")
    repair_failures = 0
    for name, required, mutate in REPAIR_MUTATIONS:
        try:
            changed = copy.deepcopy(candidate)
            before = copy.deepcopy(changed)
            mutate(changed)
            if changed == before:
                raise ValueError("mutation did not change candidate")
            findings = _check_contract(changed, authority, _canonical_json(changed))
            isolatedRows = [row for row in findings if row.startswith(required)]
        except Exception as exc:                       # noqa: BLE001 - reported
            print(f"  ESCAPE  {name}: harness raised {type(exc).__name__}: {exc}")
            repair_failures += 1
            continue
        if not isolatedRows:
            repair_failures += 1
        print(f"  {'reject' if isolatedRows else 'ESCAPE':>6}  "
              f"{name} -> {required}")

    print("\nobject mutations - every row must have a structural finding")
    escaped = 0
    for name, mutate in OBJECT_MUTATIONS:
        try:
            changed = copy.deepcopy(candidate)
            before = copy.deepcopy(changed)
            mutate(changed)
            if changed == before:
                raise ValueError("mutation did not change candidate")
            findings = _check_contract(changed, authority, _canonical_json(changed))
            structural = [row for row in findings if not row.startswith(RAW_PREFIX)]
        except Exception as exc:                       # noqa: BLE001 - reported
            print(f"  ESCAPE  {name}: harness raised {type(exc).__name__}: {exc}")
            escaped += 1
            continue
        if not structural:
            escaped += 1
        print(f"  {'reject' if structural else 'ESCAPE':>6}  {name}")

    raw_rows = _raw_mutations(candidate, candidate_source)
    raw_failures = 0
    print("\nraw mutations - every row must raise the canonical-raw layer")
    for name, changed_source in raw_rows:
        passed = False
        try:
            if changed_source == candidate_source:
                raise ValueError("raw mutation did not change candidate")
            changed = _parse_json_bytes(changed_source, name)
            findings = _check_contract(changed, authority, changed_source)
            passed = any(row.startswith(RAW_PREFIX) for row in findings)
        except (AuthorityLoadError, TypeError, ValueError):
            passed = False
        raw_failures += 0 if passed else 1
        print(f"  {'pass' if passed else 'FAIL':>6}  {name}")

    trust = _trust_order_probes(loader)
    trust_failures = sum(0 if passed else 1 for _name, passed in trust)
    print(f"\ntrust order: {len(trust) - trust_failures}/{len(trust)} pin "
          "corruptions blocked before callback")

    hostile = _hostile_candidates(candidate)
    hostile_failures = 0
    hostile_first = ""
    for name, value in hostile:
        try:
            try:
                source = _canonical_json(value)
            except (TypeError, ValueError):
                source = b""
            findings = _check_contract(value, authority, source)
        except Exception:                              # noqa: BLE001 - reported
            findings = []
        if not findings:
            hostile_failures += 1
            hostile_first = hostile_first or name
    print(f"hostile JSON shapes: {len(hostile) - hostile_failures}/{len(hostile)} "
          f"rejected without escape{'; first ' + hostile_first if hostile_first else ''}")

    print("\nretained v1.13 suite with observed child census")
    retained_result, retained_children = _retained_v113_selftest(
        candidate, authority)
    census = _child_census_findings(retained_children)
    print(f"  {'pass' if retained_result == 0 else 'FAIL':>6}  "
          "retained v1.13 selftest")
    print(f"  {'pass' if not census else 'FAIL':>6}  "
          f"{len(retained_children)} retained children conform to the declared "
          f"census{'; ' + census[0] if census else ''}")

    clean_refusal, refusal_detail = _clean_nonisolated_refusal()
    isolated_control, isolated_detail = _isolated_environment_control()
    dirty_exit, dirty_detail = _dirty_base_exit_control()
    checker_source = (HERE / CHECKER).read_bytes()
    weakened_startup = checker_source.replace(
        b"if sys.flags.isolated != 1:\n", b"if False:\n", 1)
    startup_guard = bool(_startup_source_findings(weakened_startup)) and \
        not _startup_source_findings(checker_source)
    weakened_suite = checker_source.replace(
        b"for name, required, mutate in REPAIR_MUTATIONS:",
        b"for name, required, mutate in []:", 1)
    suite_guard = bool(_selftest_reachability_findings(weakened_suite)) and \
        not _selftest_reachability_findings(checker_source)
    print("\nprocess-start and liveness controls")
    print(f"  {'pass' if clean_refusal else 'FAIL':>6}  "
          f"clean nonisolated refusal ({refusal_detail})")
    print(f"  {'pass' if isolated_control else 'FAIL':>6}  "
          f"isolated PYTHONPATH marker control ({isolated_detail})")
    print(f"  {'pass' if dirty_exit else 'FAIL':>6}  "
          f"dirty base exits 3 from a fresh process ({dirty_detail})")
    print(f"  {'pass' if startup_guard else 'FAIL':>6}  "
          "startup guard source mutation rejected")
    print(f"  {'pass' if suite_guard else 'FAIL':>6}  "
          "emptied repair suite rejected by the reachability guard")

    rt14_passed, rt14_detail, rt14_children = _rt14_rebind_probe()
    rt14_children_ok = len(rt14_children) == 2 and all(
        row["argv"] == ISOLATED_PREFIX and not row["pythonEnvironmentKeys"]
        for row in rt14_children)
    print("\ndisposable frozen RT14 checker-API probe")
    print(f"  {'pass' if rt14_passed else 'FAIL':>6}  {rt14_detail}")
    print(f"  {'pass' if rt14_children_ok else 'FAIL':>6}  "
          "RT14 children isolated and sanitized")

    failed = bool(
        repair_failures or escaped or raw_failures or trust_failures or
        hostile_failures or retained_result != 0 or census or
        not startup_flags or not clean_refusal or not isolated_control or
        not dirty_exit or not startup_guard or not suite_guard or
        not rt14_passed or not rt14_children_ok)
    print()
    if failed:
        print(
            f"SELFTEST-FAIL: repair={repair_failures}/{len(REPAIR_MUTATIONS)}, "
            f"object={escaped}/{len(OBJECT_MUTATIONS)}, "
            f"raw={raw_failures}/{len(raw_rows)}, "
            f"trust={trust_failures}/{len(trust)}, "
            f"hostile={hostile_failures}/{len(hostile)}, "
            f"retained={retained_result}, census={len(census)}, "
            f"startup={clean_refusal}/{isolated_control}/{dirty_exit}/"
            f"{startup_guard}/{suite_guard}, "
            f"rt14={rt14_passed}/{rt14_children_ok}")
        return 1
    print(
        f"SELFTEST-PASS: {len(REPAIR_MUTATIONS)} repair mutations each rejected "
        f"by their own named check; {len(OBJECT_MUTATIONS)} object and "
        f"{len(raw_rows)} raw mutations rejected; {len(trust)} pin corruptions "
        f"blocked before callback; {len(hostile)} hostile shapes rejected; "
        f"{len(retained_children)} retained children matched the declared "
        f"census; the retained v1.13 suite and the disposable RT14 normal plus "
        "selftest passed; a dirty base exits 3 from a fresh process")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED / "
          "AWAITING-INDEPENDENT-REVIEW; no seal, freeze, integration or "
          "product acceptance is declared")
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
        return selftest(
            candidate, candidate_source, authority, DeferredAuthorityLoader())
    findings = _check_contract(candidate, authority, candidate_source)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    print(
        f"D9 v1.14 contract OK - {path.name}; isolated caller trust root; "
        f"{len(PINS)} pins verified before retained execution; exact canonical "
        "raw bytes and ordered v1.13 projection; the semantic delta is exactly "
        "the two authorized repair paths; every pre-reduction cause value is "
        f"inside its closed axis enum; {GOLDEN_COUNT} goldens, {MATRIX_COUNT} "
        f"core-completion rows and {REDUCTION_COUNT} reduction records rederive "
        "identically to pinned v1.13; complete frozen RT14 API")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED / "
          "AWAITING-INDEPENDENT-REVIEW; no seal, freeze, integration or "
          "product acceptance is declared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
