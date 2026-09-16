#!/usr/bin/env python3
"""Closed successor checker for d9-exit-contract.v1.8.json.

v1.8 repairs one lifecycle hole and nothing else: authorized custody may become
unavailable after Attempt admission but before the authoritative Run commit.
The request remains REQUEST.UNSATISFIABLE, with the admitted ExecutionId and no
Run identity.  It is not reclassified as a host, CAS, ledger, or commit fault.

The checker:

  D19  exports and executes the v1.8 class/code derivation over every inherited
       golden, the new golden, and four retained CoreCompletion rows;
  D20  enforces X11, the closed union, exact identity effects, unchanged fault
       precedence, and the old-derivation falsifier;
  D21  projects the candidate mechanically to exact v1.7, runs the pinned v1.7
       checker, and compares against a fully constructed expected successor.

Usage: python3 -B artifacts/check-d9-v1.8.py [contract] [--selftest]
Exit: 0 clean · 1 findings · 2 input/JSON error
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any, Callable


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "d9-exit-contract.v1.8.json"
PREDECESSOR = "d9-exit-contract.v1.7.json"
V16_ARTIFACT = "d9-exit-contract.v1.6.json"
EXPECTED_VERSION = "v1.8"
EXPECTED_STATUS = (
    "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW "
    "(v1.8 post-admission authorized-custody-loss repair over v1.7)"
)
EXPECTED_PURPOSE = (
    "Total host-owned process-exit contract: HostTermination union, derivation "
    "rules, schema-complete golden fixtures with prohibited-effect assertions, "
    "including an admitted Run whose authorized custody loss prevents sealing."
)
EXPECTED_REQUEST_REJECTED_MEANING = (
    "Usage, configuration, admission, compatibility, lookup-address, resolver "
    "failure, mutation-precondition rejection, or an admitted Run refused before "
    "final commit because authorized retention loss made its required custody "
    "unsatisfiable."
)
EXPECTED_REMEDY = (
    "restore or restate the unavailable required authority and submit a fresh "
    "attempt; do not retry final commit of a terminal Attempt"
)
EXPECTED_REFERENCE_IMPLEMENTATION = (
    "artifacts/check-d9-v1.8.py::derive_class+derive_codes"
)
REPRODUCE = (
    "python3 -B artifacts/check-d9-v1.8.py         # defaults to the binding "
    "v1.8 artifact"
)
MUTATION_PROOF = (
    "python3 -B artifacts/check-d9-v1.8.py --selftest  # retains v1.7 proofs "
    "and rejects the closed v1.8 lifecycle mutations"
)
EXPECTED_CLAIM = (
    "Every golden and retained CoreCompletion-matrix row has its class, full "
    "code payload and exit code reproduced by the v1.8 pure derivation."
)
ACL_GOLDEN_ID = "analysis-post-admission-authorized-custody-loss"
ACL_INVARIANT_ID = "invariant-post-admission-authorized-custody-loss"
ACL_CONTRACT_KEY = "authorizedCustodyLossContract"
ACL_STATUS = "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW"
ACL_EXECUTION = "$EXEC_ID"
ACL_CODE = "REQUEST.UNSATISFIABLE"
ACL_CLASS = "request-rejected"
ACL_EXIT = 2
ACL_AUTHORITY = "NON-AUTHORITATIVE-ATTEMPT-DIAGNOSTIC"
FORBIDDEN_PUBLIC_EFFECTS = [
    "runId",
    "runSealRef",
    "terminalRunCasRef",
    "TerminalRunV1",
    "RunIndexV1",
    "RunCustodyRootV1",
    "RunAuthorityIndexV1",
    "AttemptRunLinkV1",
    "run-committed-outbox",
]
PINS = {
    "d9-exit-contract.v1.6.json":
        "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    "check-d9.py":
        "9f8e16a0000e59d2f1326f97f1b8afcc5c7121eb0c57b6c440d76b9c401346a7",
    "d9-exit-contract.v1.7.json":
        "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    "check-d9-v1.7.py":
        "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
}


class DuplicateKeyError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(), object_pairs_hook=_pairs)


def _load_v17_checker():
    path = HERE / "check-d9-v1.7.py"
    spec = importlib.util.spec_from_file_location("opensip_check_d9_v17", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load predecessor checker: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V17 = _load_v17_checker()


def _sha_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def _acl_axes(required_coverage: str, verdict: str) -> dict[str, Any]:
    return {
        "lifecycle": "cannot-seal-coherent-run",
        "requiredCoverage": required_coverage,
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


def _acl_termination() -> dict[str, Any]:
    return {
        "class": ACL_CLASS,
        "errorCode": ACL_CODE,
        "executionId": ACL_EXECUTION,
    }


ACL_INVARIANT = {
    "id": ACL_INVARIANT_ID,
    "text": (
        "An admitted Run whose exact required custody becomes unavailable through "
        "authorized expiry before final commit terminates request-rejected/"
        "REQUEST.UNSATISFIABLE with its ExecutionId and no Run identity; it is "
        "neither a host fault nor a durability-commit failure."
    ),
}
X11 = {
    "id": "X11",
    "rule": (
        "commandKind == run AND admission == admitted AND lifecycle == "
        "cannot-seal-coherent-run AND domainCondition == precondition-failed AND "
        "rejectionCause == unsatisfiable -> class == request-rejected, durability "
        "== not-applicable, requiredPostconditions == not-applicable, deficiency "
        "== none, faultCause == none"
    ),
    "why": (
        "Authorized expiry after admission is the same unsatisfiable-request "
        "remedy as pre-admission authorized loss, but its truthful lifecycle "
        "retains ExecutionId and cannot be forced through an operational fault axis."
    ),
}
ACL_GOLDEN = {
    "id": ACL_GOLDEN_ID,
    "commandKind": "run",
    "scenario": (
        "an admitted analysis has a completed core result and an exact prepared "
        "proof closure, but an explicit retention expiry deferred under its HELD "
        "lease is applied on release or crash reclaim; a fresh exact repin finds "
        "required authority unavailable, so the host refuses finalization before "
        "attempting the six-record authoritative commit"
    ),
    "scenarioAxes": _acl_axes("satisfied", "pass"),
    "expectedTermination": _acl_termination(),
    "expectedEffects": {
        "computedResult": {
            "requiredCoverage": "satisfied",
            "verdict": "pass",
            "authority": ACL_AUTHORITY,
        },
        "durability": "NOT-ATTEMPTED-PRECONDITION-REFUSAL",
        "forbiddenPublicEffects": list(FORBIDDEN_PUBLIC_EFFECTS),
        "retry": (
            "the settled ExecutionId is terminal; restored custody is used only "
            "by a fresh Attempt with a new ExecutionId"
        ),
    },
}


def _matrix_row(row_id: str, coverage: str, verdict: str) -> dict[str, Any]:
    return {
        "id": row_id,
        "axes": _acl_axes(coverage, verdict),
        "expectedTermination": _acl_termination(),
        "expectedExitCode": ACL_EXIT,
        "computedResultAuthority": ACL_AUTHORITY,
        "expectedPublicRunRecords": [],
    }


ACL_MATRIX = [
    _matrix_row("ACL-MATRIX-PASS", "satisfied", "pass"),
    _matrix_row("ACL-MATRIX-POLICY-FAIL", "satisfied", "fail"),
    _matrix_row("ACL-MATRIX-ADVISORY", "satisfied", "advisory"),
    _matrix_row("ACL-MATRIX-INDETERMINATE", "unsatisfied", "indeterminate"),
]
ACL_PREDICATE = {
    "commandKind": "run",
    "admission": "admitted",
    "lifecycle": "cannot-seal-coherent-run",
    "domainCondition": "precondition-failed",
    "rejectionCause": "unsatisfiable",
}
ACL_CONTRACT = {
    "id": "D9-V18-POST-ADMISSION-AUTHORIZED-CUSTODY-LOSS",
    "status": ACL_STATUS,
    "sourceCondition": (
        "After Attempt admission and CoreCompletion, an explicit retention expiry "
        "deferred by the exact HELD custody lease is applied on release or crash "
        "reclaim; a fresh exact repin proves at least one required authority "
        "object EXPIRED or PURGED before the final authoritative transaction begins."
    ),
    "derivationBranch": {
        "orderedAfter": [
            "admission-rejected",
            "domainCondition-host-fault",
            "signal-before-finalization",
        ],
        "orderedBefore": "run-analysis-fallback",
        "predicate": ACL_PREDICATE,
        "derivedClass": ACL_CLASS,
        "doesNotBroaden": (
            "An unrelated admitted Run precondition, a durability failure, a CAS "
            "materialization fault, host I/O, corruption or contention does not "
            "satisfy this predicate."
        ),
    },
    "remedyEquivalence": {
        "code": ACL_CODE,
        "preAdmission": (
            "restore or restate required authority before asking for an "
            "authoritative Run"
        ),
        "postAdmission": (
            "restore or restate required authority and submit a fresh Attempt"
        ),
        "sameAutomationDisposition": (
            "The current request cannot be completed under its frozen authoritative "
            "target; changing or restoring prerequisites and resubmitting is required."
        ),
        "distinctFrom": [
            "same-Attempt final-transaction retry",
            "CAS store repair",
            "transient host I/O retry",
            "ledger contention retry",
            "integrity repair",
        ],
    },
    "identityContract": {
        "requiredTerminationIdentity": "executionId",
        "forbiddenPublicIdentitiesAndRecords": list(FORBIDDEN_PUBLIC_EFFECTS),
        "retry": (
            "The settled ExecutionId is terminal. Any later attempt after authority "
            "restoration receives a new ExecutionId; semantic identities remain "
            "independent of either ExecutionId."
        ),
        "computedResult": (
            "Coverage and verdict already returned by CoreCompletion remain visible "
            "only as NON-AUTHORITATIVE-ATTEMPT-DIAGNOSTIC values. They are not a "
            "Run verdict and cannot mint a Run identity."
        ),
    },
    "retainedCoreCompletionMatrix": ACL_MATRIX,
    "faultPrecedenceControl": {
        "conditions": {
            "faultCauses": ["durability-commit"],
            "rejectionCauses": ["unsatisfiable"],
            "deficiencies": ["provider-unavailable"],
        },
        "expectedFamily": "faultCause",
        "expectedCause": "durability-commit",
        "rule": (
            "The existing faultCause > rejectionCause > deficiency reducer is "
            "byte-identical and remains authoritative."
        ),
    },
    "nonClaims": [
        "no E8 rejoin",
        "no RT13 rejoin",
        "no OP6 rejoin",
        "no claim-register update",
        "no narrative update",
        "no product disposition",
        "no integration",
        "no application",
        "no seal",
    ],
}
PEER_REVIEW_FIRST = (
    "Blind re-authoring of the axes for a sample of the 45 goldens by an agent "
    "who did not write them — the v1.3 co-consistency trap is structural and "
    "only a second author closes it."
)
PEER_REVIEW_V18 = (
    "A reviewer who authored neither v1.8 nor the pending E8, RT13 or OP6 rejoin "
    "must verify stable input hashes, the old-versus-new derivation falsifier, "
    "exact v1.8-to-v1.7 projection, union and identity negatives, and every "
    "affected consumer join before application."
)
KNOWN_COUNT = (
    "45 goldens exercise every cause enum value at least once, but not every "
    "combination of the remaining nine axes. Full cross-product is 10^5-ish and "
    "would not be more convincing."
)
KNOWN_RESIDUAL = (
    "E8, RT13 and OP6 have not been rejoined to v1.8. This candidate supplies "
    "only the termination derivation and explicitly grants no integration, "
    "application, product or seal authority."
)


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


def _is_acl(ax: dict[str, Any]) -> bool:
    return all(ax.get(key) == value for key, value in ACL_PREDICATE.items())


def derive_class(ax: dict[str, Any]) -> str:
    """Pure v1.8 axes -> HostTermination class; first matching branch wins."""
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
    if _is_acl(ax):
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
    """Pure v1.8 axes -> complete code payload."""
    cls = derive_class(ax)
    if ax["deficiency"] != "none":
        codes = [maps["deficiencyToReasonCode"][ax["deficiency"]]]
        codes += [maps["deficiencyToReasonCode"][item]
                  for item in ax.get("secondaryDeficiencies", [])]
        return {"reasonCodes": codes}
    if ax["rejectionCause"] != "none":
        return {"errorCode": maps["rejectionCauseToErrorCode"][
            ax["rejectionCause"]]}
    if ax["faultCause"] != "none":
        return {"errorCode": maps["faultCauseToErrorCode"][ax["faultCause"]]}
    if cls in ("success", "policy-failed", "interrupted"):
        return {}
    return {}


def reduce_concurrent(conditions: dict[str, Any], precedence: list[str]) -> dict[str, Any]:
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


def _golden(root: dict[str, Any], golden_id: str) -> dict[str, Any] | None:
    rows = root.get("goldenCases")
    if not isinstance(rows, list):
        return None
    matches = [row for row in rows
               if isinstance(row, dict) and row.get("id") == golden_id]
    return matches[0] if len(matches) == 1 else None


def _expected_successor(predecessor: dict[str, Any]) -> dict[str, Any]:
    expected = copy.deepcopy(predecessor)
    expected["version"] = EXPECTED_VERSION
    expected["status"] = EXPECTED_STATUS
    expected["supersedes"] = PREDECESSOR
    expected["purpose"] = EXPECTED_PURPOSE
    request_rejected = next(
        row for row in expected["exitClasses"]
        if row.get("class") == "request-rejected"
    )
    request_rejected["meaning"] = EXPECTED_REQUEST_REJECTED_MEANING
    expected["codeVocabulary"]["remedies"][ACL_CODE] = EXPECTED_REMEDY
    expected["referenceDerivation"]["implementation"] = \
        EXPECTED_REFERENCE_IMPLEMENTATION
    expected["conformanceClaims"] = [{
        "claim": EXPECTED_CLAIM,
        "reproduce": REPRODUCE,
        "mutationProof": MUTATION_PROOF,
    }]
    invariant_index = next(
        index for index, row in enumerate(expected["invariants"])
        if row.get("id") == "invariant-runid-commit-visibility"
    ) + 1
    expected["invariants"].insert(invariant_index, copy.deepcopy(ACL_INVARIANT))
    expected["goldenCases"].append(copy.deepcopy(ACL_GOLDEN))
    expected["peerReviewRequired"][0] = PEER_REVIEW_FIRST
    expected["peerReviewRequired"].append(PEER_REVIEW_V18)
    expected["knownLimitations"][3] = KNOWN_COUNT
    expected["knownLimitations"].append(KNOWN_RESIDUAL)
    expected["crossAxisInvariants"].append(copy.deepcopy(X11))
    expected[ACL_CONTRACT_KEY] = copy.deepcopy(ACL_CONTRACT)
    return expected


def _project_v17(candidate: dict[str, Any], predecessor: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(candidate)
    projected.pop(ACL_CONTRACT_KEY)
    for key in ("version", "status", "supersedes", "purpose"):
        projected[key] = copy.deepcopy(predecessor[key])
    projected["exitClasses"] = copy.deepcopy(predecessor["exitClasses"])
    projected["codeVocabulary"]["remedies"].pop(ACL_CODE)
    projected["referenceDerivation"] = copy.deepcopy(
        predecessor["referenceDerivation"])
    projected["conformanceClaims"] = copy.deepcopy(
        predecessor["conformanceClaims"])
    projected["invariants"] = [
        row for row in projected["invariants"]
        if row.get("id") != ACL_INVARIANT_ID
    ]
    projected["goldenCases"] = [
        row for row in projected["goldenCases"]
        if row.get("id") != ACL_GOLDEN_ID
    ]
    projected["peerReviewRequired"] = copy.deepcopy(
        predecessor["peerReviewRequired"])
    projected["knownLimitations"] = copy.deepcopy(
        predecessor["knownLimitations"])
    projected["crossAxisInvariants"] = [
        row for row in projected["crossAxisInvariants"]
        if row.get("id") != "X11"
    ]
    return projected


def _first_difference(actual: Any, expected: Any, path: str = "$") -> str | None:
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


def _validate_axes(label: str, axes: Any, schema: dict[str, Any],
                   findings: list[str]) -> bool:
    if not isinstance(axes, dict):
        findings.append(f"D19 {label}: axes must be an object")
        return False
    for key in axes:
        if key not in schema:
            findings.append(f"D19 {label}: undeclared axis {key!r}")
    for key, declaration in schema.items():
        if declaration.get("required") and key not in axes:
            findings.append(f"D19 {label}: missing required axis {key!r}")
    for key, value in axes.items():
        declaration = schema.get(key)
        if declaration is None:
            continue
        if value is None:
            findings.append(f"D19 {label}: axis {key!r} is explicitly null")
        elif isinstance(value, list):
            allowed = declaration.get("items", {}).get("enum", [])
            if not all(isinstance(item, str) and item in allowed for item in value):
                findings.append(f"D19 {label}: axis {key!r} has invalid list value")
        elif "enum" in declaration and value not in declaration["enum"]:
            findings.append(f"D19 {label}: axis {key!r}={value!r} is outside enum")
    return True


def _validate_termination(label: str, termination: Any,
                          contract: dict[str, Any], findings: list[str]) -> None:
    if not isinstance(termination, dict):
        findings.append(f"D19 {label}: termination must be an object")
        return
    variants = {
        row["class"]: row for row in contract["hostTerminationUnion"]["variants"]
    }
    cls = termination.get("class")
    variant = variants.get(cls)
    if variant is None:
        findings.append(f"D19 {label}: unknown termination class {cls!r}")
        return
    allowed = {"class"} | set(variant["required"]) | set(
        variant.get("optional", []))
    extra = set(termination) - allowed
    if extra:
        findings.append(f"D19 {label}: union fields not allowed: {sorted(extra)}")
    missing = set(variant["required"]) - set(termination)
    if missing:
        findings.append(f"D19 {label}: union fields missing: {sorted(missing)}")
    for key, value in termination.items():
        if value is None:
            findings.append(f"D19 {label}: termination field {key!r} is null")
    types = contract["hostTerminationUnion"]["fieldTypes"]
    for key, value in termination.items():
        if key == "class" or key not in types:
            continue
        expected_type = types[key]["type"]
        if expected_type == "string" and not isinstance(value, str):
            findings.append(f"D19 {label}: termination field {key!r} is not string")
        if expected_type == "array" and (
                not isinstance(value, list) or not value or
                not all(isinstance(item, str) for item in value)):
            findings.append(f"D19 {label}: termination field {key!r} is not nonempty string array")
        if expected_type == "object" and not isinstance(value, dict):
            findings.append(f"D19 {label}: termination field {key!r} is not object")
    vocab = set(contract["codeVocabulary"]["reasonCodes"]) | set(
        contract["codeVocabulary"]["errorCodes"])
    for code in list(termination.get("reasonCodes", [])) + (
            [termination["errorCode"]] if "errorCode" in termination else []):
        if code not in vocab:
            findings.append(f"D19 {label}: code {code!r} outside closed vocabulary")


def _x11(label: str, axes: dict[str, Any], cls: str,
         termination: dict[str, Any], findings: list[str]) -> None:
    if not _is_acl(axes):
        return
    expected_axes = {
        "durability": "not-applicable",
        "requiredPostconditions": "not-applicable",
        "deficiency": "none",
        "faultCause": "none",
    }
    if cls != ACL_CLASS:
        findings.append(f"D20 {label}: X11 derived {cls!r}, expected {ACL_CLASS!r}")
    for key, value in expected_axes.items():
        if axes.get(key) != value:
            findings.append(f"D20 {label}: X11 requires {key}={value!r}")
    if termination.get("executionId") != ACL_EXECUTION:
        findings.append(f"D20 {label}: X11 requires exact admitted ExecutionId")
    if "runId" in termination:
        findings.append(f"D20 {label}: X11 forbids RunId")


def _derive_row(label: str, axes: Any, termination: Any,
                contract: dict[str, Any], findings: list[str],
                expected_exit: int | None = None) -> None:
    schema = contract["scenarioAxesSchema"]["properties"]
    if not _validate_axes(label, axes, schema, findings) or \
            not isinstance(termination, dict):
        _validate_termination(label, termination, contract, findings)
        return
    _validate_termination(label, termination, contract, findings)
    try:
        cls = derive_class(axes)
        codes = derive_codes(axes, contract["codeMaps"])
    except (KeyError, TypeError, ValueError) as exc:
        findings.append(f"D19 {label}: derivation raised {type(exc).__name__}")
        return
    if termination.get("class") != cls:
        findings.append(
            f"D19 {label}: derived class {cls!r}, termination carries "
            f"{termination.get('class')!r}"
        )
    for field in ("errorCode", "reasonCodes"):
        if termination.get(field) != codes.get(field):
            findings.append(
                f"D19 {label}: derived {field}={codes.get(field)!r}, "
                f"termination carries {termination.get(field)!r}"
            )
    exit_code = contract["classToExitCode"].get(cls)
    if expected_exit is not None and exit_code != expected_exit:
        findings.append(
            f"D19 {label}: derived exit {exit_code!r}, expected {expected_exit!r}"
        )
    legacy_cross: list[str] = []
    V17.V16._cross_axis(label, axes, cls, legacy_cross)
    findings.extend(f"D19 inherited cross-axis: {item}" for item in legacy_cross)
    _x11(label, axes, cls, termination, findings)


def _semantic_checks(candidate: dict[str, Any], predecessor: dict[str, Any],
                     findings: list[str]) -> None:
    cases = candidate.get("goldenCases")
    if not isinstance(cases, list):
        findings.append("D19: goldenCases must be an array")
        return
    identifiers: set[str] = set()
    for row in cases:
        if not isinstance(row, dict):
            findings.append("D19: golden row must be an object")
            continue
        label = str(row.get("id", "?"))
        if label in identifiers:
            findings.append(f"D19 {label}: duplicate golden id")
        identifiers.add(label)
        if not row.get("scenario"):
            findings.append(f"D19 {label}: scenario sentence absent")
        axes = row.get("scenarioAxes")
        if isinstance(axes, dict) and row.get("commandKind") != axes.get("commandKind"):
            findings.append(f"D19 {label}: top-level/axis commandKind mismatch")
        if isinstance(axes, dict) and axes.get("projectionScope") == \
                "host-finalization-only":
            projection = row.get("hostFinalizationProjection") or {}
            if projection.get("preservesSettledRun") is not True or \
                    projection.get("doesNotClaimUniversalLifecycle") is not True:
                findings.append(f"D19 {label}: dishonest host-finalization projection")
        _derive_row(label, axes, row.get("expectedTermination"),
                    candidate, findings)

    inherited = {row["id"]: row for row in predecessor["goldenCases"]}
    for identifier, row in inherited.items():
        actual = _golden(candidate, identifier)
        if actual is None:
            findings.append(f"D19 {identifier}: inherited golden absent or duplicated")
            continue
        axes = row["scenarioAxes"]
        if derive_class(axes) != V17.V16.derive_class(axes):
            findings.append(f"D19 {identifier}: inherited class derivation changed")
        if derive_codes(axes, candidate["codeMaps"]) != \
                V17.V16.derive_codes(axes, predecessor["codeMaps"]):
            findings.append(f"D19 {identifier}: inherited code derivation changed")

    acl = candidate.get(ACL_CONTRACT_KEY)
    if not isinstance(acl, dict):
        findings.append(f"D20: {ACL_CONTRACT_KEY} must be an object")
        return
    matrix = acl.get("retainedCoreCompletionMatrix")
    if not isinstance(matrix, list):
        findings.append("D20: retained CoreCompletion matrix must be an array")
    else:
        for row in matrix:
            if not isinstance(row, dict):
                findings.append("D20: matrix row must be an object")
                continue
            _derive_row(
                str(row.get("id", "?")), row.get("axes"),
                row.get("expectedTermination"), candidate, findings,
                row.get("expectedExitCode") if isinstance(
                    row.get("expectedExitCode"), int) else None,
            )
            if row.get("computedResultAuthority") != ACL_AUTHORITY:
                findings.append(f"D20 {row.get('id', '?')}: computed result gained authority")
            if row.get("expectedPublicRunRecords") != []:
                findings.append(f"D20 {row.get('id', '?')}: public Run record escaped")

    golden = _golden(candidate, ACL_GOLDEN_ID)
    if golden is None:
        findings.append(f"D20: {ACL_GOLDEN_ID} absent or duplicated")
    else:
        old_class = V17.V16.derive_class(golden["scenarioAxes"])
        if old_class != "operational-failed":
            findings.append(
                f"D20: old-derivation falsifier did not fire; got {old_class!r}"
            )
        effects = golden.get("expectedEffects") or {}
        if effects.get("forbiddenPublicEffects") != FORBIDDEN_PUBLIC_EFFECTS:
            findings.append("D20: exact forbidden Run identity/record set drifted")

    control = acl.get("faultPrecedenceControl") or {}
    reduced = reduce_concurrent(
        control.get("conditions") or {},
        list((candidate.get("causeModel") or {}).get("precedence") or []),
    )
    if reduced.get("faultCause") != control.get("expectedCause") or \
            control.get("expectedFamily") != "faultCause" or \
            reduced.get("rejectionCause") != "none" or \
            reduced.get("deficiency") != "none":
        findings.append("D20: fault > rejection > deficiency control failed")


def check(candidate: object, predecessor: object, v16: object) -> list[str]:
    if not isinstance(candidate, dict) or not candidate:
        return ["D9-TOTALITY-ROOT: v1.8 candidate must be a nonempty object"]
    if not isinstance(predecessor, dict) or not predecessor:
        return ["D21-PREDECESSOR: v1.7 predecessor must be a nonempty object"]
    if not isinstance(v16, dict) or not v16:
        return ["D21-PREDECESSOR: v1.6 retained input must be a nonempty object"]
    findings: list[str] = []
    try:
        for filename, expected_hash in PINS.items():
            actual_hash = _sha_file(filename)
            if actual_hash != expected_hash:
                findings.append(
                    f"D21-PIN: {filename} {actual_hash} != {expected_hash}"
                )

        expected = _expected_successor(predecessor)
        try:
            projected = _project_v17(candidate, predecessor)
        except (AttributeError, KeyError, TypeError, ValueError) as exc:
            findings.append(
                f"D21-PROJECTION: cannot project v1.8 to v1.7 "
                f"({type(exc).__name__})"
            )
            projected = None
        if projected is not None:
            difference = _first_difference(projected, predecessor)
            if difference:
                findings.append(
                    "D21-PROJECTION: v1.8 does not project exactly to pinned v1.7; "
                    f"first difference: {difference}"
                )
            retained = V17.check(projected, v16)
            findings.extend(
                f"D0..D18 retained checker: {finding}" for finding in retained
            )

        # Explicit non-expansion guards make the architectural compatibility
        # claim visible even though D21 exact-delta comparison also covers it.
        if candidate.get("classToExitCode") != predecessor.get("classToExitCode"):
            findings.append("D20: classToExitCode changed")
        if candidate.get("hostTerminationUnion") != predecessor.get("hostTerminationUnion"):
            findings.append("D20: HostTermination union shape changed")
        if candidate.get("scenarioAxesSchema") != predecessor.get("scenarioAxesSchema"):
            findings.append("D20: scenario axes schema changed")
        if candidate.get("codeMaps") != predecessor.get("codeMaps"):
            findings.append("D20: cause/code maps changed")
        if candidate.get("causeModel") != predecessor.get("causeModel"):
            findings.append("D20: fault/rejection/deficiency precedence changed")
        if candidate.get("classToExitCode", {}).get(ACL_CLASS) != ACL_EXIT:
            findings.append("D20: authorized-loss exit is not exact request-rejected/2")
        before_vocab = predecessor.get("codeVocabulary") or {}
        after_vocab = candidate.get("codeVocabulary") or {}
        for key in ("reasonCodes", "errorCodes"):
            if after_vocab.get(key) != before_vocab.get(key):
                findings.append(f"D20: closed {key} vocabulary changed")
        remedies = copy.deepcopy(before_vocab.get("remedies") or {})
        remedies[ACL_CODE] = EXPECTED_REMEDY
        if after_vocab.get("remedies") != remedies:
            findings.append("D20: remedy delta is not exactly REQUEST.UNSATISFIABLE")

        _semantic_checks(candidate, predecessor, findings)
        difference = _first_difference(candidate, expected)
        if difference:
            findings.append(
                "D21-EXACT-DELTA: candidate differs outside the closed v1.8 "
                f"successor; first difference: {difference}"
            )
    except (AttributeError, IndexError, KeyError, StopIteration, TypeError,
            ValueError) as exc:
        findings.append(
            f"D9-TOTALITY-EXCEPTION: malformed parsed shape "
            f"({type(exc).__name__})"
        )
    return findings


def _mut_golden(root: dict[str, Any]) -> dict[str, Any]:
    row = _golden(root, ACL_GOLDEN_ID)
    if row is None:
        raise KeyError(ACL_GOLDEN_ID)
    return row


def _set_operational(root: dict[str, Any], cause: str, code: str,
                     domain: str = "host-fault") -> None:
    row = _mut_golden(root)
    axes = row["scenarioAxes"]
    axes["domainCondition"] = domain
    axes["rejectionCause"] = "none"
    axes["faultCause"] = cause
    row["expectedTermination"] = {
        "class": "operational-failed", "errorCode": code,
        "executionId": ACL_EXECUTION,
    }


Mutation = tuple[str, Callable[[dict[str, Any]], None]]
MUTATIONS: list[Mutation] = [
    ("version", lambda root: root.__setitem__("version", "v1.7")),
    ("status promotion", lambda root: root.__setitem__("status", "APPLIED")),
    ("supersedes", lambda root: root.__setitem__("supersedes", "d9-exit-contract.v1.6.json")),
    ("purpose", lambda root: root.__setitem__("purpose", "generic mapper")),
    ("old reference derivation", lambda root: root["referenceDerivation"].__setitem__("implementation", "artifacts/check-d9.py::derive")),
    ("drop derive_codes authority", lambda root: root["referenceDerivation"].__setitem__("implementation", "artifacts/check-d9-v1.8.py::derive_class")),
    ("drop custody-loss contract", lambda root: root.pop(ACL_CONTRACT_KEY)),
    ("old branch order", lambda root: root[ACL_CONTRACT_KEY]["derivationBranch"].__setitem__("orderedBefore", "signal-before-finalization")),
    ("branch before host fault", lambda root: root[ACL_CONTRACT_KEY]["derivationBranch"]["orderedAfter"].remove("domainCondition-host-fault")),
    ("broaden branch", lambda root: root[ACL_CONTRACT_KEY]["derivationBranch"]["predicate"].pop("rejectionCause")),
    ("operational branch declaration", lambda root: root[ACL_CONTRACT_KEY]["derivationBranch"].__setitem__("derivedClass", "operational-failed")),
    ("change unsatisfiable remedy", lambda root: root["codeVocabulary"]["remedies"].__setitem__(ACL_CODE, "retry same commit")),
    ("delete unsatisfiable remedy", lambda root: root["codeVocabulary"]["remedies"].pop(ACL_CODE)),
    ("add new public code", lambda root: root["codeVocabulary"]["errorCodes"].append("CUSTODY.UNAVAILABLE")),
    ("add new exit class", lambda root: root["classToExitCode"].__setitem__("custody-failed", 5)),
    ("renumber request rejection", lambda root: root["classToExitCode"].__setitem__(ACL_CLASS, 4)),
    ("union admits RunId", lambda root: next(row for row in root["hostTerminationUnion"]["variants"] if row["class"] == ACL_CLASS)["optional"].append("runId")),
    ("drop lifecycle invariant", lambda root: root.__setitem__("invariants", [row for row in root["invariants"] if row.get("id") != ACL_INVARIANT_ID])),
    ("weaken X11", lambda root: next(row for row in root["crossAxisInvariants"] if row["id"] == "X11").__setitem__("rule", "anything goes")),
    ("drop golden", lambda root: root.__setitem__("goldenCases", [row for row in root["goldenCases"] if row.get("id") != ACL_GOLDEN_ID])),
    ("blind operational UNSAT", lambda root: _mut_golden(root)["expectedTermination"].__setitem__("class", "operational-failed")),
    ("blind durability classification", lambda root: _set_operational(root, "durability-commit", "DURABILITY.COMMIT_FAILED")),
    ("blind CAS classification", lambda root: _set_operational(root, "cas-link", "CAS.LINK_FAILED")),
    ("blind host-I/O classification", lambda root: _set_operational(root, "host-io", "HOST.IO_FAILURE")),
    ("blind ledger-busy classification", lambda root: _set_operational(root, "ledger-busy", "LEDGER.BUSY_TIMEOUT")),
    ("rewrite as pre-admission", lambda root: (_mut_golden(root)["scenarioAxes"].__setitem__("admission", "rejected"), _mut_golden(root)["scenarioAxes"].__setitem__("lifecycle", "pre-run"), _mut_golden(root)["expectedTermination"].pop("executionId"))),
    ("drop ExecutionId", lambda root: _mut_golden(root)["expectedTermination"].pop("executionId")),
    ("inject RunId", lambda root: _mut_golden(root)["expectedTermination"].__setitem__("runId", "$RUN_ID")),
    ("mark durability failed", lambda root: _mut_golden(root)["scenarioAxes"].__setitem__("durability", "failed")),
    ("use REQUEST.PRECONDITION_FAILED", lambda root: (_mut_golden(root)["scenarioAxes"].__setitem__("rejectionCause", "precondition-failed"), _mut_golden(root)["expectedTermination"].__setitem__("errorCode", "REQUEST.PRECONDITION_FAILED"))),
    ("drop forbidden identity", lambda root: _mut_golden(root)["expectedEffects"]["forbiddenPublicEffects"].remove("RunAuthorityIndexV1")),
    ("allow same-Attempt retry", lambda root: _mut_golden(root)["expectedEffects"].__setitem__("retry", "retry same ExecutionId")),
    ("drop CoreCompletion matrix", lambda root: root[ACL_CONTRACT_KEY].__setitem__("retainedCoreCompletionMatrix", [])),
    ("matrix policy class", lambda root: root[ACL_CONTRACT_KEY]["retainedCoreCompletionMatrix"][1]["expectedTermination"].__setitem__("class", "policy-failed")),
    ("matrix gains Run record", lambda root: root[ACL_CONTRACT_KEY]["retainedCoreCompletionMatrix"][0]["expectedPublicRunRecords"].append("RunIndexV1")),
    ("matrix result gains authority", lambda root: root[ACL_CONTRACT_KEY]["retainedCoreCompletionMatrix"][0].__setitem__("computedResultAuthority", "AUTHORITATIVE")),
    ("reverse fault precedence", lambda root: root["causeModel"].__setitem__("precedence", ["rejectionCause", "faultCause", "deficiency"])),
    ("claim E8 rejoined", lambda root: root[ACL_CONTRACT_KEY]["nonClaims"].remove("no E8 rejoin")),
    ("drop independent review", lambda root: root["peerReviewRequired"].pop()),
    ("drop residual join", lambda root: root["knownLimitations"].pop()),
    ("unknown golden axis", lambda root: _mut_golden(root)["scenarioAxes"].__setitem__("custodyOkay", False)),
    ("null golden axis", lambda root: _mut_golden(root)["scenarioAxes"].__setitem__("durability", None)),
]


TOTALITY_CASES: list[tuple[str, Any]] = [
    ("string root", "hostile"),
    ("null root", None),
    ("array root", []),
    ("empty root", {}),
    ("string ACL contract", "hostile"),
    ("array matrix", {"matrix": []}),
]


def _semantic_mutation_probes(base: dict[str, Any]) -> list[tuple[str, bool]]:
    axes = _acl_axes("satisfied", "pass")
    expected = (ACL_CLASS, {"errorCode": ACL_CODE}, ACL_EXIT)
    old = (
        V17.V16.derive_class(axes),
        V17.V16.derive_codes(axes, base["codeMaps"]),
        base["classToExitCode"][V17.V16.derive_class(axes)],
    )
    unrelated = copy.deepcopy(axes)
    unrelated["rejectionCause"] = "precondition-failed"
    broad_predicate = all(
        unrelated.get(key) == value for key, value in ACL_PREDICATE.items()
        if key != "rejectionCause"
    )
    precedence = reduce_concurrent(
        ACL_CONTRACT["faultPrecedenceControl"]["conditions"],
        ["faultCause", "rejectionCause", "deficiency"],
    )
    reversed_precedence = reduce_concurrent(
        ACL_CONTRACT["faultPrecedenceControl"]["conditions"],
        ["rejectionCause", "faultCause", "deficiency"],
    )
    return [
        ("old v1.7 derivation differs", old != expected),
        ("blind durability tuple differs", ("operational-failed", {"errorCode": "DURABILITY.COMMIT_FAILED"}, 4) != expected),
        ("blind CAS tuple differs", ("operational-failed", {"errorCode": "CAS.LINK_FAILED"}, 4) != expected),
        ("blind host-I/O tuple differs", ("operational-failed", {"errorCode": "HOST.IO_FAILURE"}, 4) != expected),
        ("blind ledger-busy tuple differs", ("operational-failed", {"errorCode": "LEDGER.BUSY_TIMEOUT"}, 4) != expected),
        ("broadened predicate catches unrelated control", broad_predicate and not _is_acl(unrelated)),
        ("fault precedence differs when reversed", precedence["faultCause"] == "durability-commit" and reversed_precedence["rejectionCause"] == "unsatisfiable"),
    ]


def selftest(candidate: dict[str, Any], predecessor: dict[str, Any],
             v16: dict[str, Any]) -> int:
    base_findings = check(candidate, predecessor, v16)
    if base_findings:
        print(f"REFUSING to self-test: base has {len(base_findings)} finding(s)")
        for finding in base_findings[:10]:
            print("  -", finding)
        return 1

    projected = _project_v17(candidate, predecessor)
    print("retained v1.7/v1.6 mutation proof")
    if V17.selftest(projected, v16) != 0:
        return 1

    print("\nv1.8 closed-successor mutation proof — every row must be REJECTED\n")
    escaped = 0
    for name, mutate in MUTATIONS:
        changed = copy.deepcopy(candidate)
        mutate(changed)
        findings = check(changed, predecessor, v16)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — mutation survived'}")

    print("\nv1.8 semantic classifier falsifiers — every row must PASS\n")
    semantic_failures = 0
    for name, passed in _semantic_mutation_probes(candidate):
        if not passed:
            semantic_failures += 1
        print(f"  {'pass' if passed else 'FAIL':>6}  {name}")

    print("\nv1.8 parsed-shape totality — every row must be REJECTED\n")
    totality_failures = 0
    for name, value in TOTALITY_CASES:
        if name == "string ACL contract":
            changed = copy.deepcopy(candidate)
            changed[ACL_CONTRACT_KEY] = value
            findings = check(changed, predecessor, v16)
        elif name == "array matrix":
            changed = copy.deepcopy(candidate)
            changed[ACL_CONTRACT_KEY]["retainedCoreCompletionMatrix"] = value["matrix"]
            findings = check(changed, predecessor, v16)
        else:
            findings = check(value, predecessor, v16)
        if not findings:
            totality_failures += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")

    print()
    if escaped or semantic_failures or totality_failures:
        print(
            f"v1.8 failures: {escaped}/{len(MUTATIONS)} artifact mutations "
            f"escaped; {semantic_failures}/7 semantic falsifiers failed; "
            f"{totality_failures}/{len(TOTALITY_CASES)} totality cases escaped"
        )
        return 1
    print(
        f"all {len(MUTATIONS)} v1.8 artifact mutations rejected; 7 semantic "
        f"falsifiers passed; {len(TOTALITY_CASES)} totality cases rejected"
    )
    return 0


def main() -> int:
    positional = [argument for argument in sys.argv[1:] if argument != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        candidate = load(path)
        predecessor = load(HERE / PREDECESSOR)
        v16 = load(HERE / V16_ARTIFACT)
    except (OSError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError) as exc:
        print(f"cannot load D9 inputs: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    if "--selftest" in sys.argv[1:]:
        if not isinstance(candidate, dict) or not isinstance(predecessor, dict) or \
                not isinstance(v16, dict):
            print("selftest requires object roots", file=sys.stderr)
            return 1
        return selftest(candidate, predecessor, v16)

    findings = check(candidate, predecessor, v16)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    print(
        f"D9 v1.8 contract OK — {path.name}, "
        f"{len(candidate['goldenCases'])} goldens, "
        f"{len(candidate[ACL_CONTRACT_KEY]['retainedCoreCompletionMatrix'])} "
        "CoreCompletion rows, exact v1.7 projection, D0..D21 clean"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
