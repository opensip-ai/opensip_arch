#!/usr/bin/env python3
"""Closed successor checker for d9-exit-contract.v1.9.json.

v1.9 makes two repairs to the independently rejected v1.8 bytes:

* every transitive artifact/checker pin is verified before any retained checker
  is imported or executed, and executable modules are compiled from those exact
  verified byte snapshots; and
* the admitted unsatisfiable-finalization branch is honestly generic.  D9 maps
  a HOST-DERIVED normalized state and remedy but does not authenticate its
  source.  RT/E8 own the concrete authorized-retention provenance proof.

No class, code, exit, axis, union, precedence, identity, or remedy changes.

Usage: python3 -B artifacts/check-d9-v1.9.py [contract] [--selftest]
Exit: 0 clean · 1 findings/pin rejection · 2 input/JSON error
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import sys
import types
from dataclasses import dataclass
from typing import Any, Callable, Mapping


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "d9-exit-contract.v1.9.json"
PREDECESSOR = "d9-exit-contract.v1.8.json"
REVIEW = "d9-exit-contract.v1.8.review-independent-prefreeze.json"
EXPECTED_VERSION = "v1.9"
EXPECTED_STATUS = (
    "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW "
    "(v1.9 trust-order and generic-scope repair over rejected v1.8)"
)
EXPECTED_PURPOSE = (
    "Total host-owned process-exit contract: HostTermination union, derivation "
    "rules, schema-complete golden fixtures with prohibited-effect assertions, "
    "including any HOST-DERIVED admitted Run finalization precondition whose "
    "frozen authoritative target is proven unsatisfiable."
)
EXPECTED_REQUEST_REJECTED_MEANING = (
    "Usage, configuration, admission, compatibility, lookup-address, resolver "
    "failure, mutation-precondition rejection, or an admitted Run refused before "
    "final commit because a HOST-DERIVED finalization precondition proved its "
    "frozen authoritative target unsatisfiable."
)
REFERENCE_IMPLEMENTATION = (
    "artifacts/check-d9-v1.9.py::derive_class+derive_codes"
)
REPRODUCE = (
    "python3 -B artifacts/check-d9-v1.9.py         # defaults to the binding "
    "v1.9 artifact"
)
MUTATION_PROOF = (
    "python3 -B artifacts/check-d9-v1.9.py --selftest  # retains "
    "v1.8/v1.7/v1.6 proofs and rejects trust-order and generic-scope mutations"
)
EXPECTED_CLAIM = (
    "Every golden and retained CoreCompletion-matrix row has its class, full "
    "code payload and exit code reproduced by the v1.9 pure derivation."
)
GENERIC_CONTRACT_KEY = "hostDerivedUnsatisfiableFinalizationContract"
OLD_CONTRACT_KEY = "authorizedCustodyLossContract"
GENERIC_INVARIANT_ID = "invariant-post-admission-unsatisfiable-finalization"
OLD_INVARIANT_ID = "invariant-post-admission-authorized-custody-loss"
GOLDEN_ID = "analysis-post-admission-authorized-custody-loss"
EXECUTION_ID = "$EXEC_ID"
ERROR_CODE = "REQUEST.UNSATISFIABLE"
EXIT_CLASS = "request-rejected"
EXIT_CODE = 2
AUTHORITY = "NON-AUTHORITATIVE-ATTEMPT-DIAGNOSTIC"

PINS: dict[str, str] = {
    "d9-exit-contract.v1.8.json":
        "5fb5466372da7c8ef935a1233eb67869f21c3cdb21d67b3767159998ad26a30d",
    "check-d9-v1.8.py":
        "827e5bdd600e2682d7653bc738f07efe066f90f4d7db7bad16a7f7fd5eb91e47",
    REVIEW:
        "f044620aaac0ea4f7efc6bdd51983278bf5858f5f967b6d48310e7c0139fedb9",
    "d9-exit-contract.v1.7.json":
        "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    "check-d9-v1.7.py":
        "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
    "d9-exit-contract.v1.6.json":
        "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    "check-d9.py":
        "9f8e16a0000e59d2f1326f97f1b8afcc5c7121eb0c57b6c440d76b9c401346a7",
}
ROLES = {
    "d9-exit-contract.v1.8.json":
        "rejected predecessor data projected exactly for retained checks",
    "check-d9-v1.8.py": "retained executable checker",
    REVIEW: "independent rejection authority",
    "d9-exit-contract.v1.7.json": "retained predecessor data",
    "check-d9-v1.7.py": "transitive retained executable checker",
    "d9-exit-contract.v1.6.json": "retained predecessor data",
    "check-d9.py": "transitive retained executable checker",
}
REJECTION_FINDINGS = [
    "D9V18-PF-01-UNVERIFIED-PREDECESSOR-EXECUTION",
    "D9V18-PF-02-SOURCE-SPECIFICITY-OVERCLAIM",
]
FORBIDDEN_PUBLIC_EFFECTS = [
    "runId", "runSealRef", "terminalRunCasRef", "TerminalRunV1",
    "RunIndexV1", "RunCustodyRootV1", "RunAuthorityIndexV1",
    "AttemptRunLinkV1", "run-committed-outbox",
]
GENERIC_PREDICATE = {
    "commandKind": "run",
    "admission": "admitted",
    "lifecycle": "cannot-seal-coherent-run",
    "domainCondition": "precondition-failed",
    "rejectionCause": "unsatisfiable",
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


def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(), object_pairs_hook=_pairs)


class _VerifiedSourceLoader:
    """Minimal loader that executes one immutable, already-verified snapshot."""

    def __init__(self, filename: pathlib.Path, source: bytes):
        self.filename = filename
        self.source = source

    def create_module(self, _spec: Any) -> None:
        return None

    def exec_module(self, module: types.ModuleType) -> None:
        code = compile(self.source, str(self.filename), "exec")
        exec(code, module.__dict__)


def _execute_verified_v18(
        snapshots: Mapping[str, bytes], _parsed: Mapping[str, Any]
) -> types.ModuleType:
    """Execute v1.8/v1.7/v1.6 checkers only from verified snapshots."""
    original_spec = importlib.util.spec_from_file_location
    source_paths = {
        (HERE / name).resolve(): snapshots[name]
        for name in ("check-d9-v1.8.py", "check-d9-v1.7.py", "check-d9.py")
    }

    def verified_spec(name: str, location: Any, *args: Any,
                      **kwargs: Any) -> Any:
        try:
            resolved = pathlib.Path(location).resolve()
        except (OSError, TypeError, ValueError):
            return original_spec(name, location, *args, **kwargs)
        source = source_paths.get(resolved)
        if source is None:
            return original_spec(name, location, *args, **kwargs)
        loader = _VerifiedSourceLoader(resolved, source)
        kwargs = dict(kwargs)
        kwargs["loader"] = loader
        return original_spec(name, resolved, *args, **kwargs)

    importlib.util.spec_from_file_location = verified_spec
    try:
        path = (HERE / "check-d9-v1.8.py").resolve()
        loader = _VerifiedSourceLoader(path, snapshots["check-d9-v1.8.py"])
        spec = original_spec(
            "opensip_check_d9_v18_verified", path, loader=loader
        )
        if spec is None or spec.loader is None:
            raise AuthorityLoadError("cannot construct verified v1.8 module spec")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        importlib.util.spec_from_file_location = original_spec

    # v1.8's retained pin checker now consumes the same verified snapshots, not
    # a second executable/data read from the filesystem.
    module._sha_file = lambda name: hashlib.sha256(snapshots[name]).hexdigest()
    return module


@dataclass(frozen=True)
class Authority:
    snapshots: Mapping[str, bytes]
    predecessor: dict[str, Any]
    v17: dict[str, Any]
    v16: dict[str, Any]
    review: dict[str, Any]
    v18_checker: types.ModuleType


ReadBytes = Callable[[pathlib.Path], bytes]
ImportCallback = Callable[
    [Mapping[str, bytes], Mapping[str, Any]], Any
]


class DeferredAuthorityLoader:
    """Read+verify all transitive bytes before invoking executable authority."""

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
            for name in (PREDECESSOR, REVIEW,
                         "d9-exit-contract.v1.7.json",
                         "d9-exit-contract.v1.6.json")
        }
        review = parsed[REVIEW]
        if not isinstance(review, dict) or \
                (review.get("verdict") or {}).get("decision") != "REJECT":
            raise AuthorityLoadError("pinned v1.8 review is not a REJECT authority")
        subjects = {
            row.get("path"): row.get("sha256")
            for row in (review.get("reviewBinding") or {}).get(
                "exactSubjects", [])
            if isinstance(row, dict)
        }
        if subjects != {
            PREDECESSOR: PINS[PREDECESSOR],
            "check-d9-v1.8.py": PINS["check-d9-v1.8.py"],
        }:
            raise AuthorityLoadError("review exactSubjects do not bind pinned v1.8")
        blockers = [
            row.get("id") for row in review.get("blockingFindings", [])
            if isinstance(row, dict)
        ]
        if blockers != REJECTION_FINDINGS:
            raise AuthorityLoadError("review blocking findings drifted")
        return parsed

    def invoke_verified(self, callback: ImportCallback,
                        byte_reader: ReadBytes | None = None
                        ) -> tuple[Mapping[str, bytes], Mapping[str, Any], Any]:
        # There is deliberately no callback reference on either failure path.
        snapshots = self._snapshots(byte_reader)
        parsed = self._parsed(snapshots)
        result = callback(snapshots, parsed)
        return snapshots, parsed, result

    def load(self) -> Authority:
        snapshots, parsed, module = self.invoke_verified(_execute_verified_v18)
        if not isinstance(module, types.ModuleType):
            raise AuthorityLoadError("verified importer did not return a module")
        return Authority(
            snapshots=snapshots,
            predecessor=parsed[PREDECESSOR],
            v17=parsed["d9-exit-contract.v1.7.json"],
            v16=parsed["d9-exit-contract.v1.6.json"],
            review=parsed[REVIEW],
            v18_checker=module,
        )


def _axes(coverage: str, verdict: str) -> dict[str, Any]:
    return {
        "lifecycle": "cannot-seal-coherent-run",
        "requiredCoverage": coverage,
        "verdict": verdict,
        "durability": "not-applicable",
        "interruption": "none",
        "requiredPostconditions": "not-applicable",
        "domainCondition": "precondition-failed",
        "admission": "admitted",
        "commandKind": "run",
        "deficiency": "none",
        "rejectionCause": "unsatisfiable",
        "faultCause": "none",
        "secondaryDeficiencies": [],
    }


def _termination() -> dict[str, Any]:
    return {
        "class": EXIT_CLASS,
        "errorCode": ERROR_CODE,
        "executionId": EXECUTION_ID,
    }


def _matrix_row(row_id: str, coverage: str, verdict: str) -> dict[str, Any]:
    return {
        "id": row_id,
        "axes": _axes(coverage, verdict),
        "expectedTermination": _termination(),
        "expectedExitCode": EXIT_CODE,
        "computedResultAuthority": AUTHORITY,
        "expectedPublicRunRecords": [],
    }


GENERIC_INVARIANT = {
    "id": GENERIC_INVARIANT_ID,
    "text": (
        "Any HOST-DERIVED admitted Run finalization precondition whose frozen "
        "authoritative target is proven unsatisfiable terminates request-rejected/"
        "REQUEST.UNSATISFIABLE with its ExecutionId and no Run identity. D9 maps "
        "that normalized state and its fresh-Attempt remedy; it does not "
        "authenticate source or provenance."
    ),
}
GENERIC_X11 = {
    "id": "X11",
    "rule": (
        "commandKind == run AND admission == admitted AND lifecycle == "
        "cannot-seal-coherent-run AND domainCondition == precondition-failed AND "
        "rejectionCause == unsatisfiable -> class == request-rejected, durability "
        "== not-applicable, requiredPostconditions == not-applicable, deficiency "
        "== none, faultCause == none"
    ),
    "why": (
        "Every HOST-DERIVED admitted finalization precondition already classified "
        "unsatisfiable has the same fresh-Attempt remedy. D9 consumes that "
        "normalized classification without authenticating provenance; the owning "
        "domain contract must prove the frozen authoritative target cannot complete."
    ),
}
GOLDEN_SCENARIO = (
    "concrete retention consumer profile: an admitted analysis has a completed "
    "core result and an exact prepared proof closure, but an explicit retention "
    "expiry deferred under its HELD lease is applied on release or crash reclaim; "
    "a fresh exact repin finds required authority unavailable, so the owning RT/E8 "
    "producer proves the frozen authoritative target unsatisfiable and the host "
    "refuses finalization before attempting the six-record authoritative commit"
)
GOLDEN_RETRY = (
    "the settled ExecutionId is terminal; restored required authority is used "
    "only by a fresh Attempt with a new ExecutionId"
)
PEER_REVIEW = (
    "A reviewer who authored neither v1.9 nor the pending E8, RT14 or OP6 rejoin "
    "must verify stable input hashes, hash-before-import ordering with an "
    "uninvoked marker on pin mismatch, exact v1.9-to-v1.8 and retained "
    "v1.8-to-v1.7 projections, generic scope honesty, union and identity "
    "negatives, and every affected consumer join before application."
)
KNOWN_RESIDUAL = (
    "E8, RT14 and OP6 have not been rejoined to v1.9. D9 consumes a HOST-DERIVED "
    "unsatisfiable-finalization classification but does not mechanically prove "
    "its provenance; the owning domain contract must do so. This candidate grants "
    "no integration, application, product or seal authority."
)


def _rejected_predecessor() -> dict[str, Any]:
    return {
        "artifact": {"path": PREDECESSOR, "sha256": PINS[PREDECESSOR]},
        "checker": {
            "path": "check-d9-v1.8.py",
            "sha256": PINS["check-d9-v1.8.py"],
        },
        "independentReview": {
            "path": REVIEW,
            "sha256": PINS[REVIEW],
            "verdict": "REJECT",
        },
        "blockingFindings": list(REJECTION_FINDINGS),
        "effect": (
            "v1.9 supersedes the exact rejected v1.8 candidate and checker bytes "
            "for future review. It neither modifies nor accepts those frozen bytes."
        ),
    }


def _trust_contract() -> dict[str, Any]:
    return {
        "id": "D9-V19-HASH-BEFORE-EXECUTION",
        "transitiveInputs": [
            {"path": name, "sha256": digest, "role": ROLES[name]}
            for name, digest in PINS.items()
        ],
        "requiredOrder": [
            "read every transitive input as inert bytes",
            "verify every byte snapshot against its pinned SHA-256 and abort the whole load on any mismatch",
            "parse pinned data snapshots without importing executable dependencies",
            "only after every pin and the pinned review's rejection binding are clean invoke the injectable authority-import callback",
            "compile and execute only the already-verified checker byte snapshots; never re-read executable source for evaluation",
        ],
        "failureRule": (
            "Any transitive read, pin, data-snapshot parse, or pinned-review "
            "rejection-binding failure prevents the authority-import callback "
            "from being invoked."
        ),
        "probe": (
            "The v1.9 selftest injects both a byte reader that corrupts one "
            "transitive checker and an import callback with a marker; the mismatch "
            "must be reported and the marker count must remain zero."
        ),
    }


def _generic_contract() -> dict[str, Any]:
    return {
        "id": "D9-V19-HOST-DERIVED-UNSATISFIABLE-FINALIZATION",
        "status": "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW",
        "scope": (
            "Every HOST-DERIVED normalized admitted Run finalization precondition "
            "satisfying the exact derivation predicate below. Every matching tuple "
            "receives the same REQUEST.UNSATISFIABLE and fresh-Attempt remedy."
        ),
        "upstreamProducerObligation": (
            "Before emitting rejectionCause=unsatisfiable on this admitted "
            "finalization path, the owning domain contract must mechanically prove "
            "that the Run's frozen authoritative target cannot be completed. D9 "
            "does not authenticate that source or provenance."
        ),
        "consumerProfile": {
            "goldenId": GOLDEN_ID,
            "description": (
                "Authorized retention expiry is one concrete example, not a D9 "
                "source discriminator."
            ),
            "mechanicalProvenanceOwners": ["RT", "E8"],
        },
        "derivationBranch": {
            "orderedAfter": [
                "admission-rejected", "domainCondition-host-fault",
                "signal-before-finalization",
            ],
            "orderedBefore": "run-analysis-fallback",
            "predicate": copy.deepcopy(GENERIC_PREDICATE),
            "derivedClass": EXIT_CLASS,
            "scopeHonesty": (
                "Every normalized tuple satisfying this exact predicate maps "
                "identically. D9 has no source or provenance axis and deliberately "
                "neither authenticates nor discriminates provenance."
            ),
        },
        "remedyEquivalence": {
            "code": ERROR_CODE,
            "beforeAdmission": (
                "restore or restate the unavailable required authority before "
                "asking for an authoritative Run"
            ),
            "afterAdmission": (
                "restore or restate the unavailable required authority and submit "
                "a fresh Attempt"
            ),
            "sameAutomationDisposition": (
                "The current request cannot be completed under its frozen "
                "authoritative target; changing or restoring prerequisites and "
                "resubmitting is required."
            ),
            "distinctFrom": [
                "same-Attempt final-transaction retry", "CAS store repair",
                "transient host I/O retry", "ledger contention retry",
                "integrity repair",
            ],
        },
        "identityContract": {
            "requiredTerminationIdentity": "executionId",
            "forbiddenPublicIdentitiesAndRecords": list(FORBIDDEN_PUBLIC_EFFECTS),
            "retry": (
                "The settled ExecutionId is terminal. Any later attempt after "
                "authority restoration receives a new ExecutionId; semantic "
                "identities remain independent of either ExecutionId."
            ),
            "computedResult": (
                "Coverage and verdict already returned by CoreCompletion remain "
                "visible only as NON-AUTHORITATIVE-ATTEMPT-DIAGNOSTIC values. They "
                "are not a Run verdict and cannot mint a Run identity."
            ),
        },
        "retainedCoreCompletionMatrix": [
            _matrix_row("UFP-MATRIX-PASS", "satisfied", "pass"),
            _matrix_row("UFP-MATRIX-POLICY-FAIL", "satisfied", "fail"),
            _matrix_row("UFP-MATRIX-ADVISORY", "satisfied", "advisory"),
            _matrix_row("UFP-MATRIX-INDETERMINATE", "unsatisfied", "indeterminate"),
        ],
        "faultPrecedenceControl": {
            "conditions": {
                "faultCauses": ["durability-commit"],
                "rejectionCauses": ["unsatisfiable"],
                "deficiencies": ["provider-unavailable"],
            },
            "expectedFamily": "faultCause",
            "expectedCause": "durability-commit",
            "rule": (
                "The existing faultCause > rejectionCause > deficiency reducer "
                "is byte-identical and remains authoritative."
            ),
        },
        "nonClaims": [
            "no E8 rejoin", "no RT14 rejoin", "no OP6 rejoin",
            "no claim-register update", "no narrative update",
            "no product disposition", "no integration", "no application",
            "no seal", "no provenance authentication by D9",
        ],
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


def _unique_row(rows: Any, identifier: str) -> dict[str, Any]:
    if not isinstance(rows, list):
        raise ValueError(f"rows for {identifier} are not a list")
    matches = [
        row for row in rows
        if isinstance(row, dict) and row.get("id") == identifier
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one row {identifier}, found {len(matches)}")
    return matches[0]


def _expected_successor(predecessor: dict[str, Any]) -> dict[str, Any]:
    expected = copy.deepcopy(predecessor)
    expected["version"] = EXPECTED_VERSION
    expected["status"] = EXPECTED_STATUS
    expected["supersedes"] = PREDECESSOR
    expected["purpose"] = EXPECTED_PURPOSE
    expected = _insert_after(expected, "purpose", [
        ("rejectedPredecessor", _rejected_predecessor()),
        ("checkerTrustOrderContract", _trust_contract()),
    ])
    next(row for row in expected["exitClasses"]
         if row.get("class") == EXIT_CLASS)["meaning"] = \
        EXPECTED_REQUEST_REJECTED_MEANING
    expected["referenceDerivation"]["implementation"] = REFERENCE_IMPLEMENTATION
    expected["conformanceClaims"] = [{
        "claim": EXPECTED_CLAIM,
        "reproduce": REPRODUCE,
        "mutationProof": MUTATION_PROOF,
    }]
    invariant = _unique_row(expected["invariants"], OLD_INVARIANT_ID)
    invariant.clear()
    invariant.update(copy.deepcopy(GENERIC_INVARIANT))
    golden = _unique_row(expected["goldenCases"], GOLDEN_ID)
    golden["scenario"] = GOLDEN_SCENARIO
    golden["expectedEffects"]["retry"] = GOLDEN_RETRY
    expected["peerReviewRequired"][-1] = PEER_REVIEW
    expected["knownLimitations"][-1] = KNOWN_RESIDUAL
    x11 = _unique_row(expected["crossAxisInvariants"], "X11")
    x11.clear()
    x11.update(copy.deepcopy(GENERIC_X11))
    expected.pop(OLD_CONTRACT_KEY)
    expected[GENERIC_CONTRACT_KEY] = _generic_contract()
    return expected


def _project_v18(candidate: dict[str, Any], predecessor: dict[str, Any]
                 ) -> dict[str, Any]:
    projected = copy.deepcopy(candidate)
    projected.pop("rejectedPredecessor")
    projected.pop("checkerTrustOrderContract")
    for key in ("version", "status", "supersedes", "purpose"):
        projected[key] = copy.deepcopy(predecessor[key])
    projected["exitClasses"] = copy.deepcopy(predecessor["exitClasses"])
    projected["referenceDerivation"] = copy.deepcopy(
        predecessor["referenceDerivation"])
    projected["conformanceClaims"] = copy.deepcopy(
        predecessor["conformanceClaims"])
    projected["peerReviewRequired"] = copy.deepcopy(
        predecessor["peerReviewRequired"])
    projected["knownLimitations"] = copy.deepcopy(
        predecessor["knownLimitations"])
    old_invariant = _unique_row(predecessor["invariants"], OLD_INVARIANT_ID)
    new_invariant = _unique_row(projected["invariants"], GENERIC_INVARIANT_ID)
    new_invariant.clear()
    new_invariant.update(copy.deepcopy(old_invariant))
    old_golden = _unique_row(predecessor["goldenCases"], GOLDEN_ID)
    new_golden = _unique_row(projected["goldenCases"], GOLDEN_ID)
    new_golden.clear()
    new_golden.update(copy.deepcopy(old_golden))
    old_x11 = _unique_row(predecessor["crossAxisInvariants"], "X11")
    new_x11 = _unique_row(projected["crossAxisInvariants"], "X11")
    new_x11.clear()
    new_x11.update(copy.deepcopy(old_x11))
    projected.pop(GENERIC_CONTRACT_KEY)
    projected[OLD_CONTRACT_KEY] = copy.deepcopy(predecessor[OLD_CONTRACT_KEY])
    return projected


def _first_difference(actual: Any, expected: Any,
                      path: str = "$") -> str | None:
    if type(actual) is not type(expected):
        return f"{path}: type {type(actual).__name__} != {type(expected).__name__}"
    if isinstance(actual, dict):
        if list(actual) != list(expected):
            return f"{path}: ordered keys {list(actual)!r} != {list(expected)!r}"
        for key in expected:
            difference = _first_difference(
                actual[key], expected[key], f"{path}.{key}")
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


def _is_generic(ax: dict[str, Any]) -> bool:
    return all(ax.get(key) == value for key, value in GENERIC_PREDICATE.items())


def _analysis(ax: dict[str, Any]) -> str:
    if ax["lifecycle"] == "cannot-seal-coherent-run":
        return "operational-failed"
    if ax["durability"] == "failed":
        return "operational-failed"
    if ax["requiredPostconditions"] == "failed":
        return "operational-failed"
    if ax["requiredCoverage"] in ("unsatisfied", "unknown"):
        return "indeterminate"
    if ax["verdict"] == "indeterminate":
        return "indeterminate"
    if ax["verdict"] == "fail":
        return "policy-failed"
    if ax["verdict"] in ("pass", "advisory"):
        return "success"
    return "operational-failed"


def derive_class(ax: dict[str, Any]) -> str:
    """Pure v1.9 normalized axes -> HostTermination class."""
    command = ax["commandKind"]
    if command == "serve":
        return "success" if ax["domainCondition"] in (
            "clean-shutdown", "graceful-signal-stop") else "operational-failed"
    if ax["admission"] == "rejected":
        return "operational-failed" if ax["domainCondition"] == \
            "host-fault" else "request-rejected"
    if ax["domainCondition"] == "host-fault":
        return "operational-failed"
    if ax["interruption"] == "signal-before-finalization":
        return "interrupted"
    if _is_generic(ax):
        return "request-rejected"
    if command == "mutation":
        if ax["domainCondition"] == "precondition-failed":
            return "request-rejected"
        if ax["domainCondition"] == "verification-propagated":
            return _analysis(ax)
        return "success"
    if command == "query":
        if ax["domainCondition"] == "addressed-identity-unresolved":
            return "request-rejected"
        if ax["requiredCoverage"] == "unsatisfied":
            return "indeterminate"
        return "success"
    return _analysis(ax)


def derive_codes(ax: dict[str, Any], maps: dict[str, Any]) -> dict[str, Any]:
    """Pure v1.9 normalized axes -> complete code payload."""
    cls = derive_class(ax)
    if ax["deficiency"] != "none":
        codes = [maps["deficiencyToReasonCode"][ax["deficiency"]]]
        codes += [
            maps["deficiencyToReasonCode"][item]
            for item in ax.get("secondaryDeficiencies", [])
        ]
        return {"reasonCodes": codes}
    if ax["rejectionCause"] != "none":
        return {"errorCode": maps["rejectionCauseToErrorCode"][
            ax["rejectionCause"]]}
    if ax["faultCause"] != "none":
        return {"errorCode": maps["faultCauseToErrorCode"][ax["faultCause"]]}
    if cls in ("success", "policy-failed", "interrupted"):
        return {}
    return {}


def _semantic_rows(candidate: dict[str, Any], findings: list[str]) -> None:
    rows: list[tuple[str, Any, Any, int | None]] = []
    goldens = candidate.get("goldenCases")
    if not isinstance(goldens, list):
        findings.append("D22: goldenCases must be an array")
        return
    for row in goldens:
        if not isinstance(row, dict):
            findings.append("D22: golden row must be an object")
            continue
        rows.append((str(row.get("id", "?")), row.get("scenarioAxes"),
                     row.get("expectedTermination"), None))
    generic = candidate.get(GENERIC_CONTRACT_KEY)
    if not isinstance(generic, dict):
        findings.append(f"D23: {GENERIC_CONTRACT_KEY} must be an object")
        return
    matrix = generic.get("retainedCoreCompletionMatrix")
    if not isinstance(matrix, list):
        findings.append("D23: retainedCoreCompletionMatrix must be an array")
        return
    for row in matrix:
        if not isinstance(row, dict):
            findings.append("D23: matrix row must be an object")
            continue
        rows.append((str(row.get("id", "?")), row.get("axes"),
                     row.get("expectedTermination"), row.get("expectedExitCode")))

    for label, axes, termination, expected_exit in rows:
        if not isinstance(axes, dict) or not isinstance(termination, dict):
            findings.append(f"D22 {label}: axes/termination must be objects")
            continue
        try:
            cls = derive_class(axes)
            codes = derive_codes(axes, candidate["codeMaps"])
        except (KeyError, TypeError, ValueError) as exc:
            findings.append(f"D22 {label}: derivation raised {type(exc).__name__}")
            continue
        if termination.get("class") != cls:
            findings.append(
                f"D22 {label}: derived class {cls!r} != "
                f"{termination.get('class')!r}"
            )
        for field in ("errorCode", "reasonCodes"):
            if termination.get(field) != codes.get(field):
                findings.append(
                    f"D22 {label}: derived {field}={codes.get(field)!r} != "
                    f"{termination.get(field)!r}"
                )
        if expected_exit is not None and \
                candidate["classToExitCode"].get(cls) != expected_exit:
            findings.append(f"D22 {label}: exit code mismatch")


def check(candidate: object, authority: Authority) -> list[str]:
    if not isinstance(candidate, dict) or not candidate:
        return ["D9-TOTALITY-ROOT: v1.9 candidate must be a nonempty object"]
    findings: list[str] = []
    predecessor = authority.predecessor
    try:
        expected = _expected_successor(predecessor)
        try:
            projected = _project_v18(candidate, predecessor)
        except (AttributeError, IndexError, KeyError, StopIteration, TypeError,
                ValueError) as exc:
            findings.append(
                "D24-PROJECTION: cannot project v1.9 to v1.8 "
                f"({type(exc).__name__})"
            )
            projected = None
        if projected is not None:
            difference = _first_difference(projected, predecessor)
            if difference:
                findings.append(
                    "D24-PROJECTION: v1.9 does not project exactly to rejected "
                    f"pinned v1.8; first difference: {difference}"
                )
            retained = authority.v18_checker.check(
                projected, authority.v17, authority.v16)
            findings.extend(
                f"D0..D21 retained checker: {finding}" for finding in retained
            )

        for key in ("classToExitCode", "hostTerminationUnion",
                    "scenarioAxesSchema", "codeMaps", "causeModel"):
            if candidate.get(key) != predecessor.get(key):
                findings.append(f"D23-NONEXPANSION: {key} changed")
        if OLD_CONTRACT_KEY in candidate:
            findings.append(f"D23-SCOPE: rejected key {OLD_CONTRACT_KEY} survived")
        generic = candidate.get(GENERIC_CONTRACT_KEY)
        if isinstance(generic, dict):
            if "sourceCondition" in generic or "doesNotBroaden" in \
                    (generic.get("derivationBranch") or {}):
                findings.append("D23-SCOPE: source-specific overclaim survived")
        _semantic_rows(candidate, findings)
        difference = _first_difference(candidate, expected)
        if difference:
            findings.append(
                "D24-EXACT-DELTA: candidate differs outside the closed v1.9 "
                f"successor; first difference: {difference}"
            )
    except (AttributeError, IndexError, KeyError, StopIteration, TypeError,
            ValueError) as exc:
        findings.append(
            "D9-TOTALITY-EXCEPTION: malformed parsed shape "
            f"({type(exc).__name__})"
        )
    return findings


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def _contract(root: dict[str, Any]) -> dict[str, Any]:
    value = root[GENERIC_CONTRACT_KEY]
    if not isinstance(value, dict):
        raise TypeError(GENERIC_CONTRACT_KEY)
    return value


MUTATIONS: list[Mutation] = [
    ("version", lambda r: r.__setitem__("version", "v1.8")),
    ("status promotion", lambda r: r.__setitem__("status", "APPLIED")),
    ("wrong supersedes", lambda r: r.__setitem__("supersedes", "d9-exit-contract.v1.7.json")),
    ("generic purpose", lambda r: r.__setitem__("purpose", "generic mapper")),
    ("drop rejection binding", lambda r: r.pop("rejectedPredecessor")),
    ("accept rejected predecessor", lambda r: r["rejectedPredecessor"]["independentReview"].__setitem__("verdict", "PASS")),
    ("wrong rejection review hash", lambda r: r["rejectedPredecessor"]["independentReview"].__setitem__("sha256", "0" * 64)),
    ("drop blocker", lambda r: r["rejectedPredecessor"]["blockingFindings"].pop()),
    ("drop trust contract", lambda r: r.pop("checkerTrustOrderContract")),
    ("change transitive pin", lambda r: r["checkerTrustOrderContract"]["transitiveInputs"][1].__setitem__("sha256", "0" * 64)),
    ("drop transitive checker", lambda r: r["checkerTrustOrderContract"]["transitiveInputs"].pop()),
    ("execute before verify", lambda r: r["checkerTrustOrderContract"]["requiredOrder"].reverse()),
    ("weaken failure rule", lambda r: r["checkerTrustOrderContract"].__setitem__("failureRule", "report later")),
    ("old reference", lambda r: r["referenceDerivation"].__setitem__("implementation", "artifacts/check-d9-v1.8.py::derive_class+derive_codes")),
    ("old invariant", lambda r: _unique_row(r["invariants"], GENERIC_INVARIANT_ID).__setitem__("id", OLD_INVARIANT_ID)),
    ("source-specific X11", lambda r: _unique_row(r["crossAxisInvariants"], "X11").__setitem__("why", "authorized expiry only")),
    ("drop generic contract", lambda r: r.pop(GENERIC_CONTRACT_KEY)),
    ("restore old contract key", lambda r: r.__setitem__(OLD_CONTRACT_KEY, r.pop(GENERIC_CONTRACT_KEY))),
    ("sourceCondition key", lambda r: _contract(r).__setitem__("sourceCondition", "custody only")),
    ("doesNotBroaden key", lambda r: _contract(r)["derivationBranch"].__setitem__("doesNotBroaden", "unrelated excluded")),
    ("drop upstream proof", lambda r: _contract(r).pop("upstreamProducerObligation")),
    ("claim D9 authenticates", lambda r: _contract(r).__setitem__("upstreamProducerObligation", "D9 authenticates authorized expiry")),
    ("broaden predicate", lambda r: _contract(r)["derivationBranch"]["predicate"].pop("rejectionCause")),
    ("add source predicate", lambda r: _contract(r)["derivationBranch"]["predicate"].__setitem__("source", "retention")),
    ("old matrix id", lambda r: _contract(r)["retainedCoreCompletionMatrix"][0].__setitem__("id", "ACL-MATRIX-PASS")),
    ("matrix class", lambda r: _contract(r)["retainedCoreCompletionMatrix"][1]["expectedTermination"].__setitem__("class", "policy-failed")),
    ("matrix Run record", lambda r: _contract(r)["retainedCoreCompletionMatrix"][0]["expectedPublicRunRecords"].append("RunIndexV1")),
    ("source axis", lambda r: r["scenarioAxesSchema"]["properties"].__setitem__("source", {"enum": ["retention"], "required": True})),
    ("change exit", lambda r: r["classToExitCode"].__setitem__(EXIT_CLASS, 4)),
    ("union admits RunId", lambda r: next(row for row in r["hostTerminationUnion"]["variants"] if row["class"] == EXIT_CLASS)["optional"].append("runId")),
    ("code map", lambda r: r["codeMaps"]["rejectionCauseToErrorCode"].__setitem__("unsatisfiable", "HOST.IO_FAILURE")),
    ("precedence", lambda r: r["causeModel"].__setitem__("precedence", ["rejectionCause", "faultCause", "deficiency"])),
    ("drop concrete profile proof", lambda r: _unique_row(r["goldenCases"], GOLDEN_ID).__setitem__("scenario", "retention disappeared")),
    ("same Attempt retry", lambda r: _unique_row(r["goldenCases"], GOLDEN_ID)["expectedEffects"].__setitem__("retry", "retry same ExecutionId")),
    ("claim integration", lambda r: _contract(r)["nonClaims"].remove("no integration")),
    ("drop independent review", lambda r: r["peerReviewRequired"].pop()),
    ("drop residual", lambda r: r["knownLimitations"].pop()),
]


def _generic_scope_probes(candidate: dict[str, Any]) -> list[tuple[str, bool]]:
    base = _axes("satisfied", "pass")
    alternate_labels = [
        ("authorized-retention-profile", copy.deepcopy(base)),
        ("other-host-derived-profile", copy.deepcopy(base)),
    ]
    host_fault = copy.deepcopy(base)
    host_fault["domainCondition"] = "host-fault"
    host_fault["rejectionCause"] = "none"
    host_fault["faultCause"] = "host-io"
    signal = copy.deepcopy(base)
    signal["interruption"] = "signal-before-finalization"
    admission = copy.deepcopy(base)
    admission["admission"] = "rejected"
    admission["lifecycle"] = "pre-run"
    other_cause = copy.deepcopy(base)
    other_cause["rejectionCause"] = "precondition-failed"
    matrix = _contract(candidate)["retainedCoreCompletionMatrix"]
    schema = candidate["scenarioAxesSchema"]["properties"]
    return [
        ("external producer labels are intentionally non-discriminating",
         len({derive_class(axes) for _, axes in alternate_labels}) == 1 and
         all(derive_class(axes) == EXIT_CLASS for _, axes in alternate_labels)),
        ("source axis absent", "source" not in schema and
         "provenance" not in schema),
        ("all four CoreCompletion variants share remedy", len(matrix) == 4 and
         all(derive_class(row["axes"]) == EXIT_CLASS and
             derive_codes(row["axes"], candidate["codeMaps"]) ==
             {"errorCode": ERROR_CODE} for row in matrix)),
        ("host fault remains operational", derive_class(host_fault) ==
         "operational-failed"),
        ("signal remains interrupted", derive_class(signal) == "interrupted"),
        ("admission branch remains earlier", derive_class(admission) ==
         "request-rejected"),
        ("different normalized cause does not enter generic branch",
         not _is_generic(other_cause)),
        ("generic contract disclaims provenance authentication",
         "does not authenticate" in _contract(candidate)[
             "upstreamProducerObligation"]),
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
        except PinMismatch:
            rejected = True
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


HOSTILE_ROOTS: list[tuple[str, Any]] = [
    ("null", None), ("false", False), ("zero", 0), ("string", "hostile"),
    ("array", []), ("empty object", {}), ("float", 1.5), ("bytes", b"x"),
]


def _hostile_candidates(candidate: dict[str, Any]) -> list[tuple[str, Any]]:
    cases = list(HOSTILE_ROOTS)
    targets = [
        "rejectedPredecessor", "checkerTrustOrderContract", "exitClasses",
        "referenceDerivation", "conformanceClaims", "invariants", "goldenCases",
        "peerReviewRequired", "knownLimitations", "crossAxisInvariants",
        "scenarioAxesSchema", "classToExitCode", "hostTerminationUnion",
        "codeMaps", "causeModel", GENERIC_CONTRACT_KEY,
    ]
    hostile_values = [None, "hostile"]
    for key in targets:
        for value in hostile_values:
            changed = copy.deepcopy(candidate)
            changed[key] = value
            cases.append((f"{key}={type(value).__name__}", changed))
    for key in ("version", "status", "supersedes", "purpose"):
        changed = copy.deepcopy(candidate)
        changed.pop(key)
        cases.append((f"missing {key}", changed))
    return cases


def selftest(candidate: dict[str, Any], authority: Authority,
             loader: DeferredAuthorityLoader) -> int:
    base_findings = check(candidate, authority)
    if base_findings:
        print(f"REFUSING to self-test: base has {len(base_findings)} finding(s)")
        for finding in base_findings[:12]:
            print("  -", finding)
        return 1

    projected = _project_v18(candidate, authority.predecessor)
    print("retained v1.8/v1.7/v1.6 mutation proof")
    if authority.v18_checker.selftest(
            projected, authority.v17, authority.v16) != 0:
        return 1

    print("\nv1.9 closed-successor mutation proof — every row must be REJECTED\n")
    escaped = 0
    for name, mutate in MUTATIONS:
        changed = copy.deepcopy(candidate)
        try:
            mutate(changed)
            findings = check(changed, authority)
        except Exception as exc:  # mutation harness failure is never a pass
            findings = []
            print(f"  ESCAPE  {name}\n          mutation raised {type(exc).__name__}")
            escaped += 1
            continue
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — mutation survived'}")

    print("\nv1.9 trust-order probes — mismatch callbacks must remain uninvoked\n")
    trust_failures = 0
    trust_probes = _trust_order_probes(loader)
    for name, passed in trust_probes:
        trust_failures += 0 if passed else 1
        print(f"  {'pass' if passed else 'FAIL':>6}  {name}")

    print("\nv1.9 generic-scope controls — every row must PASS\n")
    scope_failures = 0
    scope_probes = _generic_scope_probes(candidate)
    for name, passed in scope_probes:
        scope_failures += 0 if passed else 1
        print(f"  {'pass' if passed else 'FAIL':>6}  {name}")

    print("\nv1.9 hostile parsed shapes — every row must be REJECTED\n")
    hostile_failures = 0
    hostile = _hostile_candidates(candidate)
    for name, value in hostile:
        try:
            findings = check(value, authority)
        except Exception as exc:
            findings = []
            print(f"    FAIL  {name}: raised {type(exc).__name__}")
        if not findings:
            hostile_failures += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")

    print()
    if escaped or trust_failures or scope_failures or hostile_failures:
        print(
            f"v1.9 failures: {escaped}/{len(MUTATIONS)} artifact mutations "
            f"escaped; {trust_failures}/{len(trust_probes)} trust probes failed; "
            f"{scope_failures}/{len(scope_probes)} scope controls failed; "
            f"{hostile_failures}/{len(hostile)} hostile shapes escaped"
        )
        return 1
    print(
        f"all {len(MUTATIONS)} v1.9 artifact mutations rejected; "
        f"{len(trust_probes)} trust-order probes and {len(scope_probes)} "
        f"generic-scope controls passed; {len(hostile)} hostile shapes rejected"
    )
    return 0


def main() -> int:
    positional = [arg for arg in sys.argv[1:] if arg != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        candidate = load(path)
    except (OSError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError) as exc:
        print(f"cannot load D9 candidate: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2

    loader = DeferredAuthorityLoader()
    try:
        authority = loader.load()
    except PinMismatch as exc:
        print(f"D25-PIN: retained authority rejected before import: {exc}")
        return 1
    except AuthorityLoadError as exc:
        print(f"cannot load retained D9 authority: {exc}", file=sys.stderr)
        return 2

    if "--selftest" in sys.argv[1:]:
        if not isinstance(candidate, dict):
            print("selftest requires an object root", file=sys.stderr)
            return 1
        return selftest(candidate, authority, loader)

    findings = check(candidate, authority)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    print(
        f"D9 v1.9 contract OK — {path.name}, "
        f"{len(candidate['goldenCases'])} goldens, "
        f"{len(candidate[GENERIC_CONTRACT_KEY]['retainedCoreCompletionMatrix'])} "
        f"CoreCompletion rows, {len(PINS)} transitive pins verified before import, "
        "exact v1.8 projection, retained D0..D21 clean"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
