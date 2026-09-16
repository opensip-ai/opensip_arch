#!/usr/bin/env python3
"""API-only successor checker for d9-exit-contract.v1.10.json.

v1.10 preserves the independently passed v1.9 bytes and restores the public
``reduce_concurrent(conditions, precedence)`` export accidentally omitted by
that checker.  Its behavior is compared exhaustively with the authenticated
v1.8 implementation loaded through the pinned v1.9 trust boundary.

No class, code, exit, axis, union, map, precedence, golden, identity, generic
scope, or remedy changes are allowed.

Usage: python3 -B artifacts/check-d9-v1.10.py [contract] [--selftest]
Exit: 0 clean · 1 findings/pin rejection · 2 input/JSON error
"""
from __future__ import annotations

import copy
import hashlib
import importlib.machinery
import importlib.util
import itertools
import json
import marshal
import pathlib
import struct
import sys
import tempfile
import types
from dataclasses import dataclass
from typing import Any, Callable, Mapping


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "d9-exit-contract.v1.10.json"
PREDECESSOR = "d9-exit-contract.v1.9.json"
PREDECESSOR_CHECKER = "check-d9-v1.9.py"
PREDECESSOR_REVIEW = "d9-exit-contract.v1.9.review-independent-prefreeze.json"
V18 = "d9-exit-contract.v1.8.json"
V18_CHECKER = "check-d9-v1.8.py"
V18_REVIEW = "d9-exit-contract.v1.8.review-independent-prefreeze.json"
RT14 = "retention-tiers.v14.json"
RT14_CHECKER = "check-retention-custody-v14.py"
RT14_REVIEW = "retention-tiers.v14.review-independent-prefreeze.json"
EXPECTED_VERSION = "v1.10"
EXPECTED_STATUS = (
    "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW "
    "(v1.10 public reducer compatibility repair over independently passed v1.9)"
)
EXPECTED_PURPOSE = (
    "Total host-owned process-exit contract: preserve the independently passed "
    "v1.9 taxonomy, generic unsatisfiable-finalization scope and hash-before-"
    "execution boundary while restoring the accidentally omitted public "
    "reduce_concurrent compatibility export."
)
REFERENCE_IMPLEMENTATION = (
    "artifacts/check-d9-v1.10.py::derive_class+derive_codes+reduce_concurrent"
)
REPRODUCE = (
    "python3 -B artifacts/check-d9-v1.10.py         # defaults to the binding "
    "v1.10 artifact"
)
MUTATION_PROOF = (
    "python3 -B artifacts/check-d9-v1.10.py --selftest  # retains "
    "v1.9/v1.8/v1.7/v1.6 proofs and rejects export, equivalence, trust-order "
    "and compatibility mutations"
)
EXPECTED_CLAIM = (
    "Every golden and retained CoreCompletion-matrix row has its class, full "
    "code payload and exit code reproduced by the v1.10 pure derivation; "
    "reduce_concurrent is exhaustively equivalent to the authenticated "
    "predecessor implementation."
)
COMPATIBILITY_KEY = "v19CompatibilityDisposition"
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
    PREDECESSOR:
        "bc3c2b48d3615bc262166a698d3a3559bc2fa2fbd2f637de0dbf943309194404",
    PREDECESSOR_CHECKER:
        "956e41e279e758af5dd5e342a5404f334f6223add72abdb1340c85fafa2bd936",
    PREDECESSOR_REVIEW:
        "409e55ddcc2121da5624a112728cd2d126586411a9abe06435c64d1c02b71373",
    V18:
        "5fb5466372da7c8ef935a1233eb67869f21c3cdb21d67b3767159998ad26a30d",
    V18_CHECKER:
        "827e5bdd600e2682d7653bc738f07efe066f90f4d7db7bad16a7f7fd5eb91e47",
    V18_REVIEW:
        "f044620aaac0ea4f7efc6bdd51983278bf5858f5f967b6d48310e7c0139fedb9",
    "d9-exit-contract.v1.7.json":
        "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    "check-d9-v1.7.py":
        "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
    "d9-exit-contract.v1.6.json":
        "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    "check-d9.py":
        "9f8e16a0000e59d2f1326f97f1b8afcc5c7121eb0c57b6c440d76b9c401346a7",
    RT14:
        "b66d0275d326cdd0cfdbec5e0810788e7768c10c9f1d7ab2c4df8c44b6975770",
    RT14_CHECKER:
        "6b190a89ba1700cf820746b473e8e3a521c9b2f6b4856f0c501d72a44b0a1d60",
    RT14_REVIEW:
        "dfb037bd121f7b73fbfeb77bbbaf0e1028a8c89318c5991bb3b3ec935046575c",
}
ROLES = {
    PREDECESSOR:
        "independently passed predecessor data projected exactly for retained checks",
    PREDECESSOR_CHECKER: "retained executable predecessor checker",
    PREDECESSOR_REVIEW: "independent narrow PASS authority for v1.9",
    V18:
        "rejected predecessor data projected exactly for retained checks",
    V18_CHECKER: "retained executable checker",
    V18_REVIEW: "independent rejection authority",
    "d9-exit-contract.v1.7.json": "retained predecessor data",
    "check-d9-v1.7.py": "transitive retained executable checker",
    "d9-exit-contract.v1.6.json": "retained predecessor data",
    "check-d9.py": "transitive retained executable checker",
    RT14: "inert consumer contract declaring the required public checker API",
    RT14_CHECKER: "inert consumer checker source proving reduce_concurrent is invoked",
    RT14_REVIEW: "consumer review fork guard requiring public API compatibility",
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


def _execute_snapshot(name: str, filename: str,
                      source: bytes) -> types.ModuleType:
    """Execute one fresh module from verified bytes, ignoring sys.modules/pyc."""
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


def _execute_verified_v19(
        snapshots: Mapping[str, bytes], _parsed: Mapping[str, Any]
) -> tuple[types.ModuleType, Any]:
    """Execute v1.9 and build its authority entirely from verified snapshots."""
    module = _execute_snapshot(
        "opensip_check_d9_v19_verified", PREDECESSOR_CHECKER,
        snapshots[PREDECESSOR_CHECKER])
    required = set(module.PINS)
    if required - set(snapshots):
        raise AuthorityLoadError(
            f"v1.9 transitive pin closure missing {sorted(required-set(snapshots))}")
    subset = {name: snapshots[name] for name in module.PINS}
    v19_parsed = module.DeferredAuthorityLoader._parsed(subset)
    v18_checker = module._execute_verified_v18(subset, v19_parsed)
    authority = module.Authority(
        snapshots=subset,
        predecessor=v19_parsed[module.PREDECESSOR],
        v17=v19_parsed["d9-exit-contract.v1.7.json"],
        v16=v19_parsed["d9-exit-contract.v1.6.json"],
        review=v19_parsed[module.REVIEW],
        v18_checker=v18_checker,
    )
    return module, authority


@dataclass(frozen=True)
class Authority:
    snapshots: Mapping[str, bytes]
    predecessor: dict[str, Any]
    predecessor_review: dict[str, Any]
    rt14: dict[str, Any]
    rt14_review: dict[str, Any]
    v19_checker: types.ModuleType
    v19_authority: Any


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
            for name in (
                PREDECESSOR, PREDECESSOR_REVIEW, V18, V18_REVIEW,
                "d9-exit-contract.v1.7.json", "d9-exit-contract.v1.6.json",
                RT14, RT14_REVIEW,
            )
        }
        review = parsed[PREDECESSOR_REVIEW]
        if not isinstance(review, dict) or \
                (review.get("verdict") or {}).get("decision") != "PASS" or \
                (review.get("hashWindow") or {}).get("inputHashDrift") is not False:
            raise AuthorityLoadError("pinned v1.9 review is not a stable PASS")
        reviewed = (review.get("hashWindow") or {}).get("reviewedInputs") or {}
        if reviewed.get("artifacts/d9-exit-contract.v1.9.json") != \
                PINS[PREDECESSOR] or \
                reviewed.get("artifacts/check-d9-v1.9.py") != \
                PINS[PREDECESSOR_CHECKER]:
            raise AuthorityLoadError("v1.9 PASS does not bind the pinned pair")

        review18 = parsed[V18_REVIEW]
        if not isinstance(review18, dict) or \
                (review18.get("verdict") or {}).get("decision") != "REJECT":
            raise AuthorityLoadError("pinned v1.8 review is not a REJECT authority")
        subjects = {
            row.get("path"): row.get("sha256")
            for row in (review18.get("reviewBinding") or {}).get(
                "exactSubjects", [])
            if isinstance(row, dict)
        }
        if subjects != {
            V18: PINS[V18], V18_CHECKER: PINS[V18_CHECKER],
        }:
            raise AuthorityLoadError("review exactSubjects do not bind pinned v1.8")
        blockers = [
            row.get("id") for row in review18.get("blockingFindings", [])
            if isinstance(row, dict)
        ]
        if blockers != REJECTION_FINDINGS:
            raise AuthorityLoadError("review blocking findings drifted")

        rt14_review = parsed[RT14_REVIEW]
        if (rt14_review.get("verdict") or {}).get("decision") != \
                "REJECTED-BY-DEPENDENCY":
            raise AuthorityLoadError("RT14 review disposition drifted")
        required = (((parsed[RT14].get("contextualD9Rejoin") or {}).get(
            "authority") or {}).get("requiredCheckerApi"))
        if required != [
                "check", "derive_class", "derive_codes", "reduce_concurrent"]:
            raise AuthorityLoadError("RT14 required public checker API drifted")
        fork_guard = ((rt14_review.get("rt15PinOnlySuccessor") or {}).get(
            "forkGuard") or "")
        if "API" not in fork_guard or "not pin-only" not in fork_guard:
            raise AuthorityLoadError("RT14 consumer API fork guard drifted")
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
        snapshots, parsed, loaded = self.invoke_verified(_execute_verified_v19)
        if not isinstance(loaded, tuple) or len(loaded) != 2 or \
                not isinstance(loaded[0], types.ModuleType):
            raise AuthorityLoadError("verified importer did not return v1.9 authority")
        module, v19_authority = loaded
        return Authority(
            snapshots=snapshots,
            predecessor=parsed[PREDECESSOR],
            predecessor_review=parsed[PREDECESSOR_REVIEW],
            rt14=parsed[RT14],
            rt14_review=parsed[RT14_REVIEW],
            v19_checker=module,
            v19_authority=v19_authority,
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
    "A reviewer who authored neither v1.10 nor the pending RT15 rebind must "
    "verify stable input hashes, exact v1.10-to-v1.9 projection, the required "
    "public export set, exhaustive reduce_concurrent equivalence against "
    "authenticated predecessor bytes, malicious pyc/path/sys.modules isolation, "
    "retained v1.9/v1.8/v1.7/v1.6 suites, and the unchanged generic-scope and "
    "taxonomy surfaces before application."
)
KNOWN_RESIDUAL = (
    "The v1.9 independent PASS remains valid for its narrow reviewed repairs but "
    "its exact checker bytes are insufficient for RT14 consumer compatibility "
    "because they omit reduce_concurrent. RT15 has not been created, and E8, "
    "RT14 and OP6 have not been rejoined to v1.10. This candidate grants no "
    "integration, application, product or seal authority."
)


def _rejected_predecessor() -> dict[str, Any]:
    return {
        "artifact": {"path": V18, "sha256": PINS[V18]},
        "checker": {
            "path": V18_CHECKER,
            "sha256": PINS[V18_CHECKER],
        },
        "independentReview": {
            "path": V18_REVIEW,
            "sha256": PINS[V18_REVIEW],
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
        "id": "D9-V110-HASH-BEFORE-EXECUTION",
        "transitiveInputs": [
            {"path": name, "sha256": digest, "role": ROLES[name]}
            for name, digest in PINS.items()
        ],
        "requiredOrder": [
            "read every transitive input as inert bytes",
            "verify every byte snapshot against its pinned SHA-256 and abort the whole load on any mismatch",
            "parse pinned data snapshots without importing executable dependencies",
            "only after every pin and both pinned D9 review verdict bindings are clean invoke the injectable authority-import callback",
            "compile and execute only the already-verified checker byte snapshots; never re-read executable source for evaluation",
        ],
        "failureRule": (
            "Any transitive read, pin, data-snapshot parse, or pinned-review "
            "verdict/binding failure prevents the authority-import callback "
            "from being invoked."
        ),
        "probe": (
            "The v1.10 selftest injects a corruption for every pinned input and "
            "an import callback with a marker; every mismatch must be reported "
            "and every marker count must remain zero."
        ),
    }


def _compatibility_disposition() -> dict[str, Any]:
    return {
        "status": "NARROW-PASS-VALID / CONSUMER-COMPATIBILITY-INCOMPLETE",
        "predecessor": {
            "artifact": PREDECESSOR,
            "artifactSha256": PINS[PREDECESSOR],
            "checker": PREDECESSOR_CHECKER,
            "checkerSha256": PINS[PREDECESSOR_CHECKER],
            "independentReview": PREDECESSOR_REVIEW,
            "independentReviewSha256": PINS[PREDECESSOR_REVIEW],
            "reviewVerdict": "PASS",
        },
        "reviewScopeStatement": (
            "The v1.9 independent PASS remains valid for its hash-before-"
            "execution and honest generic-scope repairs and is not overturned "
            "by this successor."
        ),
        "consumerCompatibilityFinding": (
            "The exact passed v1.9 checker accidentally omitted the public "
            "reduce_concurrent export required and invoked by the frozen RT14 "
            "consumer; therefore those bytes are insufficient for an RT15 "
            "pin-only rebind."
        ),
        "consumerAuthority": {
            "artifact": RT14, "artifactSha256": PINS[RT14],
            "checker": RT14_CHECKER, "checkerSha256": PINS[RT14_CHECKER],
            "independentReview": RT14_REVIEW,
            "independentReviewSha256": PINS[RT14_REVIEW],
        },
        "requiredPublicExports": [
            "check", "derive_class", "derive_codes", "reduce_concurrent",
        ],
        "repairBoundary": (
            "v1.10 restores only reduce_concurrent(conditions, precedence) with "
            "behavior exhaustively checked against the authenticated v1.8 "
            "implementation reachable through pinned v1.9 authority. No "
            "taxonomy, schema, map, precedence, golden, identity, scope or "
            "remedy changes are permitted."
        ),
        "authorityBoundary": (
            "CANDIDATE-NOT-APPLIED / NO RT15, product, claim, TM, narrative, "
            "integration, application or seal authority"
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
    expected["checkerTrustOrderContract"] = _trust_contract()
    expected = _insert_after(expected, "checkerTrustOrderContract", [
        (COMPATIBILITY_KEY, _compatibility_disposition()),
    ])
    expected["referenceDerivation"]["implementation"] = REFERENCE_IMPLEMENTATION
    expected["conformanceClaims"] = [{
        "claim": EXPECTED_CLAIM,
        "reproduce": REPRODUCE,
        "mutationProof": MUTATION_PROOF,
    }]
    expected["peerReviewRequired"][-1] = PEER_REVIEW
    expected["knownLimitations"][-1] = KNOWN_RESIDUAL
    return expected


def _project_v19(candidate: dict[str, Any], predecessor: dict[str, Any]
                 ) -> dict[str, Any]:
    projected = copy.deepcopy(candidate)
    projected.pop(COMPATIBILITY_KEY)
    for key in ("version", "status", "supersedes", "purpose"):
        projected[key] = copy.deepcopy(predecessor[key])
    projected["checkerTrustOrderContract"] = copy.deepcopy(
        predecessor["checkerTrustOrderContract"])
    projected["referenceDerivation"] = copy.deepcopy(
        predecessor["referenceDerivation"])
    projected["conformanceClaims"] = copy.deepcopy(
        predecessor["conformanceClaims"])
    projected["peerReviewRequired"] = copy.deepcopy(
        predecessor["peerReviewRequired"])
    projected["knownLimitations"] = copy.deepcopy(
        predecessor["knownLimitations"])
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
    """Pure v1.10 normalized axes -> HostTermination class."""
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
    """Pure v1.10 normalized axes -> complete code payload."""
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


def reduce_concurrent(conditions: dict[str, Any],
                      precedence: list[str]) -> dict[str, Any]:
    """Restore the public v1.8 reducer API, byte-semantically unchanged."""
    faults = list(conditions.get("faultCauses") or [])
    rejections = list(conditions.get("rejectionCauses") or [])
    deficiencies = list(conditions.get("deficiencies") or [])
    secondaries = list(conditions.get("secondaryDeficiencies") or [])
    result = {
        "faultCause": "none", "rejectionCause": "none",
        "deficiency": "none", "secondaryDeficiencies": [],
    }
    for family in precedence:
        if family == "faultCause" and faults:
            result["faultCause"] = faults[0]
            return result
        if family == "rejectionCause" and rejections:
            result["rejectionCause"] = rejections[0]
            return result
        if family == "deficiency" and deficiencies:
            result["deficiency"] = deficiencies[0]
            seen: set[str] = set()
            result["secondaryDeficiencies"] = [
                value for value in deficiencies[1:] + secondaries
                if value != deficiencies[0] and
                not (value in seen or seen.add(value))
            ]
            return result
    return result


REDUCER_EQUIVALENCE_CASE_COUNT = 61_194
_REDUCER_EQUIVALENCE_CACHE: dict[int, list[str]] = {}


def _reducer_equivalence_findings(
        candidate: dict[str, Any], authority: Authority) -> list[str]:
    """Exhaust the declared singleton space plus order/dedup edge cases."""
    cache_key = id(authority)
    if cache_key in _REDUCER_EQUIVALENCE_CACHE:
        return list(_REDUCER_EQUIVALENCE_CACHE[cache_key])
    schema = authority.predecessor["scenarioAxesSchema"]["properties"]
    faults = [
        value for value in schema["faultCause"]["enum"] if value != "none"]
    rejections = [
        value for value in schema["rejectionCause"]["enum"]
        if value != "none"]
    deficiencies = [
        value for value in schema["deficiency"]["enum"] if value != "none"]
    precedences = list(itertools.permutations(
        ["faultCause", "rejectionCause", "deficiency"]))
    predecessor_reduce = authority.v19_authority.v18_checker.reduce_concurrent
    findings: list[str] = []
    count = 0

    def compare(conditions: dict[str, Any], order: tuple[str, ...]) -> bool:
        nonlocal count
        count += 1
        actual = reduce_concurrent(copy.deepcopy(conditions), list(order))
        expected = predecessor_reduce(copy.deepcopy(conditions), list(order))
        if actual != expected:
            findings.append(
                f"D27-EQUIVALENCE: case {count} differs: {actual!r} != {expected!r}"
            )
            return False
        return True

    single_faults = [[]] + [[value] for value in faults]
    single_rejections = [[]] + [[value] for value in rejections]
    single_deficiencies = [[]] + [[value] for value in deficiencies]
    single_secondaries = [[]] + [[value] for value in deficiencies]
    for fault_rows, rejection_rows, deficiency_rows, secondary_rows, order in \
            itertools.product(
                single_faults, single_rejections, single_deficiencies,
                single_secondaries, precedences):
        if not compare({
                "faultCauses": fault_rows,
                "rejectionCauses": rejection_rows,
                "deficiencies": deficiency_rows,
                "secondaryDeficiencies": secondary_rows,
        }, order):
            break
    if not findings:
        for values, field in (
                (faults, "faultCauses"),
                (rejections, "rejectionCauses"),
                (deficiencies, "deficiencies")):
            for first in values:
                for second in values:
                    if first == second:
                        continue
                    for order in precedences:
                        conditions = {
                            "faultCauses": [], "rejectionCauses": [],
                            "deficiencies": [], "secondaryDeficiencies": [],
                        }
                        conditions[field] = [first, second]
                        if not compare(conditions, order):
                            break
                    if findings:
                        break
                if findings:
                    break
            if findings:
                break
    if not findings:
        for primary in deficiencies:
            for secondary in deficiencies:
                for order in precedences:
                    if not compare({
                            "faultCauses": [], "rejectionCauses": [],
                            "deficiencies": [primary],
                            "secondaryDeficiencies": [secondary, secondary],
                    }, order):
                        break
                if findings:
                    break
            if findings:
                break
    if not findings and count != REDUCER_EQUIVALENCE_CASE_COUNT:
        findings.append(
            f"D27-EQUIVALENCE: generated {count} cases, expected "
            f"{REDUCER_EQUIVALENCE_CASE_COUNT}"
        )
    _REDUCER_EQUIVALENCE_CACHE[cache_key] = list(findings)
    return findings


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
        return ["D9-TOTALITY-ROOT: v1.10 candidate must be a nonempty object"]
    findings: list[str] = []
    predecessor = authority.predecessor
    try:
        expected = _expected_successor(predecessor)
        try:
            projected = _project_v19(candidate, predecessor)
        except (AttributeError, IndexError, KeyError, StopIteration, TypeError,
                ValueError) as exc:
            findings.append(
                "D26-PROJECTION: cannot project v1.10 to v1.9 "
                f"({type(exc).__name__})"
            )
            projected = None
        if projected is not None:
            difference = _first_difference(projected, predecessor)
            if difference:
                findings.append(
                    "D26-PROJECTION: v1.10 does not project exactly to the "
                    f"independently passed pinned v1.9; first difference: {difference}"
                )
            retained = authority.v19_checker.check(
                projected, authority.v19_authority)
            findings.extend(
                f"D0..D25 retained checker: {finding}" for finding in retained
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
        compatibility = candidate.get(COMPATIBILITY_KEY)
        required = compatibility.get("requiredPublicExports") \
            if isinstance(compatibility, dict) else None
        exports = {
            "check": check, "derive_class": derive_class,
            "derive_codes": derive_codes,
            "reduce_concurrent": reduce_concurrent,
        }
        if required != list(exports) or not all(
                callable(exports[name]) for name in required or []):
            findings.append("D27-EXPORT: exact callable public compatibility API absent")
        if hasattr(authority.v19_checker, "reduce_concurrent"):
            findings.append("D27-HISTORY: pinned v1.9 unexpectedly already exports reducer")
        findings.extend(_reducer_equivalence_findings(candidate, authority))
        _semantic_rows(candidate, findings)
        difference = _first_difference(candidate, expected)
        if difference:
            findings.append(
                "D28-EXACT-DELTA: candidate differs outside the closed v1.10 "
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
    ("version", lambda r: r.__setitem__("version", "v1.9")),
    ("status promotion", lambda r: r.__setitem__("status", "APPLIED")),
    ("wrong supersedes", lambda r: r.__setitem__("supersedes", V18)),
    ("generic purpose", lambda r: r.__setitem__("purpose", "generic mapper")),
    ("drop compatibility disposition", lambda r: r.pop(COMPATIBILITY_KEY)),
    ("overturn v1.9 PASS", lambda r: r[COMPATIBILITY_KEY].__setitem__("status", "REJECTED")),
    ("wrong v1.9 artifact pin", lambda r: r[COMPATIBILITY_KEY]["predecessor"].__setitem__("artifactSha256", "0" * 64)),
    ("wrong v1.9 checker pin", lambda r: r[COMPATIBILITY_KEY]["predecessor"].__setitem__("checkerSha256", "0" * 64)),
    ("wrong v1.9 review pin", lambda r: r[COMPATIBILITY_KEY]["predecessor"].__setitem__("independentReviewSha256", "0" * 64)),
    ("change v1.9 review verdict", lambda r: r[COMPATIBILITY_KEY]["predecessor"].__setitem__("reviewVerdict", "REJECT")),
    ("wrong RT14 artifact pin", lambda r: r[COMPATIBILITY_KEY]["consumerAuthority"].__setitem__("artifactSha256", "0" * 64)),
    ("wrong RT14 checker pin", lambda r: r[COMPATIBILITY_KEY]["consumerAuthority"].__setitem__("checkerSha256", "0" * 64)),
    ("wrong RT14 review pin", lambda r: r[COMPATIBILITY_KEY]["consumerAuthority"].__setitem__("independentReviewSha256", "0" * 64)),
    ("drop reducer export", lambda r: r[COMPATIBILITY_KEY]["requiredPublicExports"].remove("reduce_concurrent")),
    ("reorder exports", lambda r: r[COMPATIBILITY_KEY]["requiredPublicExports"].reverse()),
    ("broaden repair", lambda r: r[COMPATIBILITY_KEY].__setitem__("repairBoundary", "change taxonomy too")),
    ("claim RT15", lambda r: r[COMPATIBILITY_KEY].__setitem__("authorityBoundary", "RT15 APPLIED")),
    ("drop trust contract", lambda r: r.pop("checkerTrustOrderContract")),
    ("change v1.9 transitive pin", lambda r: r["checkerTrustOrderContract"]["transitiveInputs"][1].__setitem__("sha256", "0" * 64)),
    ("drop consumer pin", lambda r: r["checkerTrustOrderContract"]["transitiveInputs"].pop()),
    ("execute before verify", lambda r: r["checkerTrustOrderContract"]["requiredOrder"].reverse()),
    ("weaken failure rule", lambda r: r["checkerTrustOrderContract"].__setitem__("failureRule", "report later")),
    ("old reference", lambda r: r["referenceDerivation"].__setitem__("implementation", "artifacts/check-d9-v1.9.py::derive_class+derive_codes")),
    ("drop reducer from claim", lambda r: r["conformanceClaims"][0].__setitem__("claim", "goldens only")),
    ("drop inherited rejection binding", lambda r: r.pop("rejectedPredecessor")),
    ("source-specific X11", lambda r: _unique_row(r["crossAxisInvariants"], "X11").__setitem__("why", "authorized expiry only")),
    ("drop generic contract", lambda r: r.pop(GENERIC_CONTRACT_KEY)),
    ("sourceCondition key", lambda r: _contract(r).__setitem__("sourceCondition", "custody only")),
    ("source axis", lambda r: r["scenarioAxesSchema"]["properties"].__setitem__("source", {"enum": ["retention"], "required": True})),
    ("change exit", lambda r: r["classToExitCode"].__setitem__(EXIT_CLASS, 4)),
    ("union admits RunId", lambda r: next(row for row in r["hostTerminationUnion"]["variants"] if row["class"] == EXIT_CLASS)["optional"].append("runId")),
    ("code map", lambda r: r["codeMaps"]["rejectionCauseToErrorCode"].__setitem__("unsatisfiable", "HOST.IO_FAILURE")),
    ("precedence", lambda r: r["causeModel"].__setitem__("precedence", ["rejectionCause", "faultCause", "deficiency"])),
    ("drop concrete profile proof", lambda r: _unique_row(r["goldenCases"], GOLDEN_ID).__setitem__("scenario", "retention disappeared")),
    ("same Attempt retry", lambda r: _unique_row(r["goldenCases"], GOLDEN_ID)["expectedEffects"].__setitem__("retry", "retry same ExecutionId")),
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


def _api_probes(candidate: dict[str, Any], authority: Authority
                ) -> list[tuple[str, bool]]:
    required = candidate[COMPATIBILITY_KEY]["requiredPublicExports"]
    rt_required = authority.rt14["contextualD9Rejoin"]["authority"][
        "requiredCheckerApi"]
    control = {
        "faultCauses": ["durability-commit"],
        "rejectionCauses": ["unsatisfiable"],
        "deficiencies": ["provider-unavailable"],
    }
    wrong = {
        "faultCause": "none", "rejectionCause": "unsatisfiable",
        "deficiency": "none", "secondaryDeficiencies": [],
    }
    actual = reduce_concurrent(
        control, ["faultCause", "rejectionCause", "deficiency"])
    return [
        ("v1.9 narrow PASS remains bound",
         (authority.predecessor_review.get("verdict") or {}).get(
             "decision") == "PASS"),
        ("v1.9 omission independently observable",
         not hasattr(authority.v19_checker, "reduce_concurrent")),
        ("v1.10 exact required export order", required == [
            "check", "derive_class", "derive_codes", "reduce_concurrent"]),
        ("RT14 consumer requires same export order", rt_required == required),
        ("RT14 checker invokes reducer",
         b"d9mod.reduce_concurrent(" in authority.snapshots[RT14_CHECKER]),
        ("fault precedence falsifies a rejection-first reducer",
         actual != wrong and actual.get("faultCause") == "durability-commit"),
        ("exhaustive equivalence is clean",
         not _reducer_equivalence_findings(candidate, authority)),
    ]


def _write_pyc(path: pathlib.Path, marker: pathlib.Path) -> None:
    code = compile(
        f"from pathlib import Path\nPath({str(marker)!r}).write_text('PYC')\n",
        str(path), "exec")
    header = importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, 0, 0)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(header + marshal.dumps(code))


def _environment_isolation_probes(loader: DeferredAuthorityLoader
                                  ) -> list[tuple[str, bool]]:
    probes: list[tuple[str, bool]] = []

    module_name = "opensip_check_d9_v19_verified"
    prior = sys.modules.get(module_name)
    hostile = types.ModuleType(module_name)
    hostile.reduce_concurrent = lambda *_args: {"hostile": True}
    sys.modules[module_name] = hostile
    try:
        _, _, loaded = loader.invoke_verified(_execute_verified_v19)
        passed = isinstance(loaded, tuple) and loaded[0] is not hostile and \
            not hasattr(loaded[0], "reduce_concurrent")
    except AuthorityLoadError:
        passed = False
    finally:
        if prior is None:
            sys.modules.pop(module_name, None)
        else:
            sys.modules[module_name] = prior
    probes.append(("hostile sys.modules entry ignored", passed))

    trusted = {name: (HERE / name).read_bytes() for name in PINS}
    with tempfile.TemporaryDirectory(prefix="opensip-d9-v110-path-") as raw:
        directory = pathlib.Path(raw)
        for name, source in trusted.items():
            (directory / name).write_bytes(source)
        marker = directory / "path-marker"
        malicious = trusted[PREDECESSOR_CHECKER] + (
            f"\npathlib.Path({str(marker)!r}).write_text('PATH')\n".encode())
        (directory / PREDECESSOR_CHECKER).write_bytes(malicious)
        # Establish that the swapped bytes are executable and side-effectful.
        try:
            _execute_snapshot("d9_v19_malicious_path_control",
                              PREDECESSOR_CHECKER, malicious)
            control_fired = marker.exists()
        except Exception:
            control_fired = False
        marker.unlink(missing_ok=True)
        temp_loader = DeferredAuthorityLoader(directory)

        def trusted_reader(path: pathlib.Path) -> bytes:
            return trusted[path.name]

        try:
            temp_loader.invoke_verified(_execute_verified_v19, trusted_reader)
            isolated = not marker.exists()
        except AuthorityLoadError:
            isolated = False
        probes.append(("verified snapshot defeats disk path swap",
                       control_fired and isolated))

    with tempfile.TemporaryDirectory(prefix="opensip-d9-v110-pyc-") as raw:
        directory = pathlib.Path(raw)
        for name, source in trusted.items():
            (directory / name).write_bytes(source)
        marker = directory / "pyc-marker"
        tag = sys.implementation.cache_tag or "python"
        pyc = directory / "__pycache__" / f"check-d9-v1.9.{tag}.pyc"
        _write_pyc(pyc, marker)
        try:
            importlib.machinery.SourcelessFileLoader(
                "d9_v19_malicious_pyc_control", str(pyc)).load_module()
            control_fired = marker.exists()
        except Exception:
            control_fired = False
        marker.unlink(missing_ok=True)
        try:
            DeferredAuthorityLoader(directory).load()
            isolated = not marker.exists()
        except AuthorityLoadError:
            isolated = False
        probes.append(("malicious pyc ignored in favor of verified source bytes",
                       control_fired and isolated))

    return probes


HOSTILE_ROOTS: list[tuple[str, Any]] = [
    ("null", None), ("false", False), ("zero", 0), ("string", "hostile"),
    ("array", []), ("empty object", {}), ("float", 1.5), ("bytes", b"x"),
]


def _hostile_candidates(candidate: dict[str, Any]) -> list[tuple[str, Any]]:
    cases = list(HOSTILE_ROOTS)
    targets = [
        "rejectedPredecessor", "checkerTrustOrderContract", COMPATIBILITY_KEY,
        "exitClasses",
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

    projected = _project_v19(candidate, authority.predecessor)
    print("retained v1.9/v1.8/v1.7/v1.6 mutation proof")
    if authority.v19_checker.selftest(
            projected, authority.v19_authority,
            authority.v19_checker.DeferredAuthorityLoader()) != 0:
        return 1

    print("\nv1.10 API-only successor mutations — every row must be REJECTED\n")
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

    print("\nv1.10 trust-order probes — mismatch callbacks must remain uninvoked\n")
    trust_failures = 0
    trust_probes = _trust_order_probes(loader)
    for name, passed in trust_probes:
        trust_failures += 0 if passed else 1
        print(f"  {'pass' if passed else 'FAIL':>6}  {name}")

    print("\nv1.10 API and exhaustive-equivalence controls — every row must PASS\n")
    api_failures = 0
    api_probes = _api_probes(candidate, authority)
    for name, passed in api_probes:
        api_failures += 0 if passed else 1
        print(f"  {'pass' if passed else 'FAIL':>6}  {name}")

    print("\nv1.10 malicious environment isolation — every row must PASS\n")
    environment_failures = 0
    environment_probes = _environment_isolation_probes(loader)
    for name, passed in environment_probes:
        environment_failures += 0 if passed else 1
        print(f"  {'pass' if passed else 'FAIL':>6}  {name}")

    print("\nretained v1.9 generic-scope controls — every row must PASS\n")
    scope_failures = 0
    scope_probes = _generic_scope_probes(candidate)
    for name, passed in scope_probes:
        scope_failures += 0 if passed else 1
        print(f"  {'pass' if passed else 'FAIL':>6}  {name}")

    print("\nv1.10 hostile parsed shapes — every row must be REJECTED\n")
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
    if escaped or trust_failures or api_failures or environment_failures or \
            scope_failures or hostile_failures:
        print(
            f"v1.10 failures: {escaped}/{len(MUTATIONS)} artifact mutations "
            f"escaped; {trust_failures}/{len(trust_probes)} trust probes failed; "
            f"{api_failures}/{len(api_probes)} API probes failed; "
            f"{environment_failures}/{len(environment_probes)} environment "
            f"probes failed; "
            f"{scope_failures}/{len(scope_probes)} scope controls failed; "
            f"{hostile_failures}/{len(hostile)} hostile shapes escaped"
        )
        return 1
    print(
        f"all {len(MUTATIONS)} v1.10 artifact mutations rejected; "
        f"{len(trust_probes)} trust-order, {len(api_probes)} API, and "
        f"{len(environment_probes)} environment probes passed; "
        f"{REDUCER_EQUIVALENCE_CASE_COUNT} reducer cases matched; "
        f"{len(scope_probes)} retained generic-scope controls passed; "
        f"{len(hostile)} hostile shapes rejected"
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
        print(f"D29-PIN: retained authority rejected before import: {exc}")
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
        f"D9 v1.10 contract OK — {path.name}, "
        f"{len(candidate['goldenCases'])} goldens, "
        f"{len(candidate[GENERIC_CONTRACT_KEY]['retainedCoreCompletionMatrix'])} "
        f"CoreCompletion rows, {len(PINS)} pins verified before import, "
        f"{REDUCER_EQUIVALENCE_CASE_COUNT} reducer cases equivalent, exact "
        "v1.9 projection, retained D0..D25 clean"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
