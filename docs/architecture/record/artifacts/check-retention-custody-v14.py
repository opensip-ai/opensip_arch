#!/usr/bin/env python3
"""Closed RT14 contextual-D9 successor checker.

RT14 changes no RT13 semantic/raw custody identity or reducer behavior.  It
projects exactly to pinned RT13 and adds one closed host-contextual D9 v1.8
join for authorized custody loss after Attempt admission.  The local RT
resolve-and-pin reducer remains context-free and unchanged.

This is architecture test-double evidence only.  D9 v1.8 and RT14 both remain
NOT-APPLIED and require independent frozen-byte review.
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
BINDING = "retention-tiers.v14.json"
RT13 = "retention-tiers.v13.json"
RT13_CHECKER = "check-retention-custody-v13.py"
RT_CORE = "check-retention-custody.py"
D9 = "d9-exit-contract.v1.8.json"
D9_CHECKER = "check-d9-v1.8.py"
D9_V17 = "d9-exit-contract.v1.7.json"
D9_V17_CHECKER = "check-d9-v1.7.py"
D9_V16 = "d9-exit-contract.v1.6.json"
D9_V16_CHECKER = "check-d9.py"

PINS = {
    RT13: "3f79668a6d26b5ecc7fd843be71aef90e779ac024a1ac54bb5cc2c8fc3e0a349",
    RT13_CHECKER: "0290b4ae22816843c2fbce1288ea36f21e78b396361fa6c0bf5291338be519f6",
    RT_CORE: "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
    D9: "5fb5466372da7c8ef935a1233eb67869f21c3cdb21d67b3767159998ad26a30d",
    D9_CHECKER: "827e5bdd600e2682d7653bc738f07efe066f90f4d7db7bad16a7f7fd5eb91e47",
    D9_V17: "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    D9_V17_CHECKER: "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
    D9_V16: "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    D9_V16_CHECKER: "9f8e16a0000e59d2f1326f97f1b8afcc5c7121eb0c57b6c440d76b9c401346a7",
}
RT13_CANONICAL_SHA = \
    "c79decdeb92e40fe7ec1e8f4cc2eee51f33f63dcc223f2e3b3a0908ffbf826f0"
D9_DERIVATION_SHA = \
    "fd7b659debd36f3c955cfb26a9af4a97968707d0d22fd54cb2cb275106317e87"
PROJECTION_HASHES = {
    "semanticClosure": "70ce71b8fc31551809c7c800a165fa5d9a8a8e04a7e5523e7668324fce8a977c",
    "availability": "f53af4bc27a771ef5b72a7be1b7b39b66a58b4831bf9402b47c1fcafbca22916",
    "purgeAndLineage": "09c03454779cb884d4d904df66511c45942056e6c4b22579723979bff0325145",
    "leaseProtocol": "a0023a4ab71568ceb902a0fba356d2483d152d2d3762e68541285d3f2b853c7b",
    "d9Derivation": D9_DERIVATION_SHA,
}
EXPECTED_UNCHANGED_ROOTS = [
    "artifact", "status", "claimId", "capabilityClosure", "leaseProtocol",
    "storageAndLineage", "d9Derivation", "custodyPolicy", "authority",
    "integrationState", "invariants", "assurance", "retainedResiduals",
    "sealRecommendation", "rawPhysicalIdentityContract",
    "identityStabilityFromRT12",
]
REQUIRED_SOURCE_FACTS = [
    "existing admitted ExecutionId",
    "completed CoreCompletion",
    "exact HELD lease over the RT13 23-object pin set",
    "nonempty expiryAppliedRefs from release or crash-reclaim",
    "fresh exact repin returns local REQUEST.UNSATISFIABLE",
    "at least one required raw object is EXPIRED or PURGED",
    "authoritative final transaction has not begun",
]
OUTPUT_CONSTRUCTION = [
    "Validate the exact closed axes row.",
    "Call pinned D9 v1.8 derive_class and derive_codes; do not trust stored class/code literals.",
    "Map the derived class through pinned classToExitCode.",
    "Append only the already-admitted ExecutionId and validate the closed HostTermination union.",
    "Publish no Run identity or final Run record.",
]
NON_CLAIMS = [
    "no E8 rejoin", "no OP6 rejoin", "no claim-register update",
    "no narrative update", "no product disposition", "no integration",
    "no application", "no seal",
    "no production runtime or durability demonstration",
]


class DuplicateKeyError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def load(name_or_path: str | pathlib.Path) -> Any:
    path = pathlib.Path(name_or_path)
    if not path.is_absolute() and path.parent == pathlib.Path("."):
        path = HERE / path
    return json.loads(path.read_text(), object_pairs_hook=_pairs)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def _verify_pins() -> list[str]:
    findings: list[str] = []
    for filename, expected in PINS.items():
        try:
            actual = sha_file(filename)
        except OSError as exc:
            findings.append(f"RT14-PIN: {filename} unreadable ({type(exc).__name__})")
            continue
        if actual != expected:
            findings.append(f"RT14-PIN: {filename} {actual} != {expected}")
    return findings


def _module(filename: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_AUTHORITIES: dict[str, Any] | None = None


def _authorities() -> dict[str, Any]:
    """Hash every executable dependency before its first import."""
    global _AUTHORITIES
    pin_findings = _verify_pins()
    if pin_findings:
        raise ValueError(pin_findings[0])
    if _AUTHORITIES is None:
        _AUTHORITIES = {
            "rt13": load(RT13),
            "rt13mod": _module(RT13_CHECKER, "rt14_pinned_rt13"),
            "rtcore": _module(RT_CORE, "rt14_pinned_rtcore"),
            "d9": load(D9),
            "d9mod": _module(D9_CHECKER, "rt14_pinned_d9_v18"),
            "d9v17": load(D9_V17),
            "d9v16": load(D9_V16),
        }
    return _AUTHORITIES


def _project_rt13(candidate: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(candidate)
    projected.pop("contextualD9Rejoin")
    projected["version"] = 13
    projected["supersedesAsArchitectureCandidate"] = \
        "retention-tiers.v12.json"
    return projected


def regenerate(contract: dict[str, Any], ep: dict[str, Any], epmod: Any,
               rtcore: Any) -> dict[str, Any]:
    """Preserve the v13 cold-regeneration API for E8 consumers."""
    authorities = _authorities()
    projected = _project_rt13(contract)
    if projected != authorities["rt13"]:
        raise ValueError("RT14 does not project exactly to pinned RT13")
    return authorities["rt13mod"].regenerate(projected, ep, epmod, rtcore)


def _local_axes() -> dict[str, Any]:
    return {
        "lifecycle": "pre-run",
        "requiredCoverage": "not-applicable",
        "verdict": "not-applicable",
        "durability": "not-applicable",
        "interruption": "none",
        "requiredPostconditions": "not-applicable",
        "domainCondition": "none",
        "admission": "rejected",
        "commandKind": "run",
        "deficiency": "none",
        "rejectionCause": "unsatisfiable",
        "faultCause": "none",
        "secondaryDeficiencies": [],
    }


def _expected_overlay(d9: dict[str, Any]) -> dict[str, Any]:
    acl = d9["authorizedCustodyLossContract"]
    return {
        "schemaVersion": 1,
        "status": "CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW",
        "authority": {
            "d9Artifact": D9,
            "d9ArtifactSha256": PINS[D9],
            "d9Checker": D9_CHECKER,
            "d9CheckerSha256": PINS[D9_CHECKER],
            "requiredCheckerApi": [
                "check", "derive_class", "derive_codes", "reduce_concurrent",
            ],
            "d9ReviewState": "PENDING-INDEPENDENT-REVIEW",
            "authorityClaim": "NONE",
        },
        "rt13Projection": {
            "artifact": RT13,
            "artifactSha256": PINS[RT13],
            "checker": RT13_CHECKER,
            "checkerSha256": PINS[RT13_CHECKER],
            "coreChecker": RT_CORE,
            "coreCheckerSha256": PINS[RT_CORE],
            "canonicalSha256": RT13_CANONICAL_SHA,
            "algorithm": (
                "Remove contextualD9Rejoin, restore version=13 and "
                "supersedesAsArchitectureCandidate=retention-tiers.v12.json, "
                "then require exact object equality and canonical hash equality "
                "with the pinned RT13 artifact."
            ),
            "unchangedRootKeys": list(EXPECTED_UNCHANGED_ROOTS),
            "identityProjectionSha256": copy.deepcopy(PROJECTION_HASHES),
        },
        "retainedD9Rows": {
            "source": "retention-tiers.v13.json#d9Derivation.rows",
            "count": 11,
            "canonicalD9DerivationSha256": D9_DERIVATION_SHA,
            "rule": (
                "Every retained row remains byte-exact and is independently "
                "rederived through pinned D9 v1.8 derive_class, derive_codes "
                "and classToExitCode."
            ),
        },
        "contextSplit": {
            "retentionLocalUnavailable": {
                "phase": "PRE-ADMISSION-RETENTION-LOCAL",
                "source": (
                    "The unchanged RT core resolve-and-pin reducer finds at "
                    "least one exact requested RawObjectKeyV1 absent or not "
                    "AVAILABLE."
                ),
                "axes": _local_axes(),
                "expectedReducerResult": {
                    "kind": "D9",
                    "termination": {
                        "class": "request-rejected",
                        "errorCode": "REQUEST.UNSATISFIABLE",
                    },
                },
                "expectedExitCode": 2,
                "identity": {"executionId": "ABSENT", "runId": "ABSENT"},
                "stateEffect": "UNCHANGED",
            },
            "admittedAuthorizedCustodyLoss": {
                "phase": (
                    "POST-ADMISSION-POST-CORE-BEFORE-FINAL-TRANSACTION"
                ),
                "sourceD9GoldenId": (
                    "analysis-post-admission-authorized-custody-loss"
                ),
                "sourceCondition": acl["sourceCondition"],
                "requiredSourceFacts": list(REQUIRED_SOURCE_FACTS),
                "coreCompletionMatrix": copy.deepcopy(
                    acl["retainedCoreCompletionMatrix"]),
                "outputConstruction": list(OUTPUT_CONSTRUCTION),
                "terminationIdentity": {
                    "executionId": "REQUIRED-EXISTING",
                    "runId": "FORBIDDEN",
                },
                "forbiddenPublicIdentitiesAndRecords": copy.deepcopy(
                    acl["identityContract"][
                        "forbiddenPublicIdentitiesAndRecords"]),
                "retry": acl["identityContract"]["retry"],
            },
        },
        "faultPrecedenceControl": {
            "conditions": copy.deepcopy(
                acl["faultPrecedenceControl"]["conditions"]),
            "expectedFamily": "faultCause",
            "expectedCause": "durability-commit",
        },
        "nonClaims": list(NON_CLAIMS),
    }


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


def _validate_axes(label: str, axes: Any, d9: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    schema = d9["scenarioAxesSchema"]
    declarations = schema["properties"]
    if not isinstance(axes, dict):
        return [f"{label}: axes must be a closed object"]
    if schema.get("additionalProperties") is not False:
        findings.append(f"{label}: upstream axes schema is not closed")
    for key in axes:
        if key not in declarations:
            findings.append(f"{label}: unknown axis {key!r}")
    for key, declaration in declarations.items():
        if declaration.get("required") is True and key not in axes:
            findings.append(f"{label}: missing required axis {key!r}")
    for key, value in axes.items():
        declaration = declarations.get(key)
        if declaration is None:
            continue
        if value is None:
            findings.append(f"{label}: axis {key!r} is null")
        elif declaration.get("type") == "array":
            allowed = declaration.get("items", {}).get("enum", [])
            if not isinstance(value, list) or not all(
                    isinstance(item, str) and item in allowed for item in value):
                findings.append(f"{label}: axis {key!r} has invalid array")
        elif "enum" in declaration and value not in declaration["enum"]:
            findings.append(f"{label}: axis {key!r} is outside its enum")
    return findings


def _derive(axes: dict[str, Any], d9: dict[str, Any], d9mod: Any) -> \
        tuple[dict[str, Any], int]:
    cls = d9mod.derive_class(copy.deepcopy(axes))
    codes = d9mod.derive_codes(copy.deepcopy(axes), d9["codeMaps"])
    termination = {"class": cls, **codes}
    return termination, d9["classToExitCode"][cls]


def _projection_hashes(projected: dict[str, Any]) -> dict[str, str]:
    closure = projected["capabilityClosure"]
    values = {
        "semanticClosure": closure["semanticClosure"],
        "availability": {
            "unitAvailabilityRecords": closure["unitAvailabilityRecords"],
            "availabilityFixtures": closure["availabilityFixtures"],
        },
        "purgeAndLineage": projected["storageAndLineage"],
        "leaseProtocol": projected["leaseProtocol"],
        "d9Derivation": projected["d9Derivation"],
    }
    return {key: canonical_sha(value) for key, value in values.items()}


def _retained_row_findings(projected: dict[str, Any], d9: dict[str, Any],
                           d9mod: Any) -> list[str]:
    findings: list[str] = []
    rows = projected["d9Derivation"].get("rows")
    if not isinstance(rows, list) or len(rows) != 11:
        return ["RT14-D9-RETAINED: exactly 11 retained rows required"]
    for row in rows:
        label = f"RT14-D9-RETAINED {row.get('id', '?')}"
        axes = row.get("axes")
        findings.extend(_validate_axes(label, axes, d9))
        if not isinstance(axes, dict):
            continue
        try:
            termination, exit_code = _derive(axes, d9, d9mod)
        except (KeyError, TypeError, ValueError) as exc:
            findings.append(f"{label}: derivation raised {type(exc).__name__}")
            continue
        if termination != row.get("expectedTermination"):
            findings.append(
                f"{label}: derived termination differs from retained row")
        if exit_code != row.get("expectedExitCode"):
            findings.append(f"{label}: derived exit differs from retained row")
    return findings


def _local_findings(overlay: dict[str, Any], projected: dict[str, Any],
                    d9: dict[str, Any], d9mod: Any,
                    rtcore: Any) -> list[str]:
    findings: list[str] = []
    local = overlay["contextSplit"]["retentionLocalUnavailable"]
    axes = local["axes"]
    findings.extend(_validate_axes("RT14-D9-LOCAL", axes, d9))
    derived, exit_code = _derive(axes, d9, d9mod)
    if derived != local["expectedReducerResult"]["termination"] or \
            exit_code != local["expectedExitCode"]:
        findings.append("RT14-D9-LOCAL: D9 v1.8 derivation mismatch")

    fixtures = projected["leaseProtocol"]["fixtures"]
    source = next(
        row for row in fixtures if row.get("id") == "LF-01-RESOLVE-AND-PIN")
    state = copy.deepcopy(source["initial"])
    event = copy.deepcopy(source["event"])
    requested = {
        (row["projectId"], row["recordCasRef"], row["recordKind"])
        for row in event["pinRefs"]
    }
    changed = False
    for row in state["objects"]:
        key = (row["projectId"], row["recordCasRef"], row["recordKind"])
        if key in requested:
            row["state"] = "PURGED"
            changed = True
            break
    if not changed:
        findings.append("RT14-D9-LOCAL: fixture has no requested raw object")
        return findings
    before = canonical(state)
    result = rtcore.reduce_lease(copy.deepcopy(state), event)
    if result.get("result") != local["expectedReducerResult"]:
        findings.append("RT14-D9-LOCAL: RT core local result drifted")
    if canonical(result.get("state")) != before:
        findings.append("RT14-D9-LOCAL: rejected local resolve mutated state")
    termination = result.get("result", {}).get("termination", {})
    if "executionId" in termination or "runId" in termination:
        findings.append("RT14-D9-LOCAL: local result leaked host identity")
    return findings


def _contextual_findings(overlay: dict[str, Any], d9: dict[str, Any],
                         d9mod: Any) -> list[str]:
    findings: list[str] = []
    admitted = overlay["contextSplit"]["admittedAuthorizedCustodyLoss"]
    rows = admitted["coreCompletionMatrix"]
    if not isinstance(rows, list) or len(rows) != 4:
        return ["RT14-D9-CONTEXT: exact four-row CoreCompletion matrix required"]
    for row in rows:
        label = f"RT14-D9-CONTEXT {row.get('id', '?')}"
        axes = row.get("axes")
        findings.extend(_validate_axes(label, axes, d9))
        if not isinstance(axes, dict):
            continue
        derived, exit_code = _derive(axes, d9, d9mod)
        termination = {**derived, "executionId": "$EXEC_ID"}
        if termination != row.get("expectedTermination"):
            findings.append(f"{label}: contextual termination is not derived")
        if exit_code != row.get("expectedExitCode"):
            findings.append(f"{label}: contextual exit is not derived")
        if set(termination) != {"class", "errorCode", "executionId"} or \
                "runId" in termination:
            findings.append(f"{label}: closed ExecutionId-only identity failed")
        if row.get("expectedPublicRunRecords") != []:
            findings.append(f"{label}: final Run record escaped")

    first_axes = rows[0]["axes"]
    old_class = d9mod.V17.V16.derive_class(first_axes)
    new_class = d9mod.derive_class(first_axes)
    if old_class != "operational-failed" or new_class != "request-rejected" or \
            d9["classToExitCode"][old_class] != 4 or \
            d9["classToExitCode"][new_class] != 2:
        findings.append("RT14-D9-CONTEXT: old-versus-new falsifier did not fire")

    control = overlay["faultPrecedenceControl"]
    reduced = d9mod.reduce_concurrent(
        copy.deepcopy(control["conditions"]),
        list(d9["causeModel"]["precedence"]),
    )
    if reduced != {
            "faultCause": "durability-commit", "rejectionCause": "none",
            "deficiency": "none", "secondaryDeficiencies": []}:
        findings.append("RT14-D9-CONTEXT: fault precedence drifted")
    return findings


def check(value: Any) -> list[str]:
    if not isinstance(value, dict) or not value:
        return ["RT14-TOTALITY-ROOT: candidate must be a nonempty object"]
    findings = _verify_pins()
    if findings:
        return findings
    try:
        authorities = _authorities()
        rt13 = authorities["rt13"]
        d9 = authorities["d9"]
        expected_keys = list(rt13) + ["contextualD9Rejoin"]
        if list(value) != expected_keys:
            findings.append(
                f"RT14-CLOSED-ROOT: ordered keys {list(value)!r} != "
                f"{expected_keys!r}")
        if value.get("version") != 14 or \
                value.get("supersedesAsArchitectureCandidate") != RT13 or \
                value.get("status") != "CANDIDATE-NOT-APPLIED":
            findings.append("RT14-METADATA: exact NOT-APPLIED successor metadata required")

        overlay = value.get("contextualD9Rejoin")
        if not isinstance(overlay, dict):
            findings.append("RT14-OVERLAY: contextualD9Rejoin must be a closed object")
            return findings
        expected_overlay = _expected_overlay(d9)
        difference = _first_difference(overlay, expected_overlay,
                                       "$.contextualD9Rejoin")
        if difference:
            findings.append(f"RT14-OVERLAY: closed overlay drift; {difference}")

        projected = _project_rt13(value)
        difference = _first_difference(projected, rt13, "$projectedRT13")
        if difference:
            findings.append(f"RT14-PROJECTION: not exact RT13; {difference}")
        if canonical_sha(projected) != RT13_CANONICAL_SHA:
            findings.append("RT14-PROJECTION: canonical RT13 hash drifted")
        if _projection_hashes(projected) != PROJECTION_HASHES:
            findings.append("RT14-IDENTITY: closure/availability/purge/lease/D9 bytes drifted")

        retained_rt_findings = authorities["rt13mod"].check(
            projected, verify_files=True)
        findings.extend(
            f"RT13 retained checker: {item}" for item in retained_rt_findings)
        d9_findings = authorities["d9mod"].check(
            d9, authorities["d9v17"], authorities["d9v16"])
        findings.extend(f"D9 v1.8 retained checker: {item}" for item in d9_findings)

        findings.extend(_retained_row_findings(
            projected, d9, authorities["d9mod"]))
        findings.extend(_local_findings(
            overlay, projected, d9, authorities["d9mod"],
            authorities["rtcore"]))
        findings.extend(_contextual_findings(
            overlay, d9, authorities["d9mod"]))
    except (AttributeError, IndexError, KeyError, StopIteration, TypeError,
            ValueError) as exc:
        findings.append(
            f"RT14-TOTALITY-EXCEPTION: controlled malformed shape "
            f"({type(exc).__name__})")
    return findings


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def _overlay(root: dict[str, Any]) -> dict[str, Any]:
    return root["contextualD9Rejoin"]


MUTATIONS: list[Mutation] = [
    ("version", lambda root: root.__setitem__("version", 13)),
    ("status promotion", lambda root: root.__setitem__("status", "APPLIED")),
    ("supersedes", lambda root: root.__setitem__(
        "supersedesAsArchitectureCandidate", "retention-tiers.v12.json")),
    ("unknown root", lambda root: root.__setitem__("trusted", True)),
    ("drop overlay", lambda root: root.pop("contextualD9Rejoin")),
    ("unknown overlay field", lambda root: _overlay(root).__setitem__(
        "trusted", True)),
    ("null overlay", lambda root: root.__setitem__(
        "contextualD9Rejoin", None)),
    ("D9 artifact pin", lambda root: _overlay(root)["authority"].__setitem__(
        "d9ArtifactSha256", "0" * 64)),
    ("D9 checker pin", lambda root: _overlay(root)["authority"].__setitem__(
        "d9CheckerSha256", "0" * 64)),
    ("drop derive_codes API", lambda root: _overlay(root)["authority"]
        ["requiredCheckerApi"].remove("derive_codes")),
    ("promote D9 review", lambda root: _overlay(root)["authority"].__setitem__(
        "d9ReviewState", "ACCEPTED")),
    ("claim authority", lambda root: _overlay(root)["authority"].__setitem__(
        "authorityClaim", "APPLIED")),
    ("RT13 artifact pin", lambda root: _overlay(root)["rt13Projection"]
        .__setitem__("artifactSha256", "0" * 64)),
    ("projection algorithm", lambda root: _overlay(root)["rt13Projection"]
        .__setitem__("algorithm", "trust producer")),
    ("drop unchanged root", lambda root: _overlay(root)["rt13Projection"]
        ["unchangedRootKeys"].pop()),
    ("identity projection", lambda root: _overlay(root)["rt13Projection"]
        ["identityProjectionSha256"].__setitem__("leaseProtocol", "0" * 64)),
    ("retained row count", lambda root: _overlay(root)["retainedD9Rows"]
        .__setitem__("count", 10)),
    ("retained literal rule", lambda root: _overlay(root)["retainedD9Rows"]
        .__setitem__("rule", "trust expectedTermination")),
    ("local unknown axis", lambda root: _overlay(root)["contextSplit"]
        ["retentionLocalUnavailable"]["axes"].__setitem__("pinned", True)),
    ("local admitted", lambda root: _overlay(root)["contextSplit"]
        ["retentionLocalUnavailable"]["axes"].__setitem__("admission", "admitted")),
    ("local class", lambda root: _overlay(root)["contextSplit"]
        ["retentionLocalUnavailable"]["expectedReducerResult"]["termination"]
        .__setitem__("class", "operational-failed")),
    ("local ExecutionId", lambda root: _overlay(root)["contextSplit"]
        ["retentionLocalUnavailable"]["expectedReducerResult"]["termination"]
        .__setitem__("executionId", "$EXEC_ID")),
    ("local RunId", lambda root: _overlay(root)["contextSplit"]
        ["retentionLocalUnavailable"]["expectedReducerResult"]["termination"]
        .__setitem__("runId", "$RUN_ID")),
    ("local mutates", lambda root: _overlay(root)["contextSplit"]
        ["retentionLocalUnavailable"].__setitem__("stateEffect", "MUTATED")),
    ("context phase", lambda root: _overlay(root)["contextSplit"]
        ["admittedAuthorizedCustodyLoss"].__setitem__("phase", "PRE-RUN")),
    ("drop source fact", lambda root: _overlay(root)["contextSplit"]
        ["admittedAuthorizedCustodyLoss"]["requiredSourceFacts"].pop()),
    ("drop matrix", lambda root: _overlay(root)["contextSplit"]
        ["admittedAuthorizedCustodyLoss"]["coreCompletionMatrix"].pop()),
    ("matrix class", lambda root: _overlay(root)["contextSplit"]
        ["admittedAuthorizedCustodyLoss"]["coreCompletionMatrix"][0]
        ["expectedTermination"].__setitem__("class", "operational-failed")),
    ("matrix code", lambda root: _overlay(root)["contextSplit"]
        ["admittedAuthorizedCustodyLoss"]["coreCompletionMatrix"][0]
        ["expectedTermination"].__setitem__(
            "errorCode", "DURABILITY.COMMIT_FAILED")),
    ("drop matrix ExecutionId", lambda root: _overlay(root)["contextSplit"]
        ["admittedAuthorizedCustodyLoss"]["coreCompletionMatrix"][0]
        ["expectedTermination"].pop("executionId")),
    ("matrix RunId", lambda root: _overlay(root)["contextSplit"]
        ["admittedAuthorizedCustodyLoss"]["coreCompletionMatrix"][0]
        ["expectedTermination"].__setitem__("runId", "$RUN_ID")),
    ("matrix exit", lambda root: _overlay(root)["contextSplit"]
        ["admittedAuthorizedCustodyLoss"]["coreCompletionMatrix"][0]
        .__setitem__("expectedExitCode", 4)),
    ("matrix authority", lambda root: _overlay(root)["contextSplit"]
        ["admittedAuthorizedCustodyLoss"]["coreCompletionMatrix"][0]
        .__setitem__("computedResultAuthority", "AUTHORITATIVE")),
    ("matrix public record", lambda root: _overlay(root)["contextSplit"]
        ["admittedAuthorizedCustodyLoss"]["coreCompletionMatrix"][0]
        ["expectedPublicRunRecords"].append("RunIndexV1")),
    ("literal output construction", lambda root: _overlay(root)
        ["contextSplit"]["admittedAuthorizedCustodyLoss"]
        ["outputConstruction"].__setitem__(1, "use stored class/code")),
    ("drop forbidden record", lambda root: _overlay(root)["contextSplit"]
        ["admittedAuthorizedCustodyLoss"]
        ["forbiddenPublicIdentitiesAndRecords"].pop()),
    ("same Attempt retry", lambda root: _overlay(root)["contextSplit"]
        ["admittedAuthorizedCustodyLoss"].__setitem__(
            "retry", "retry same ExecutionId")),
    ("fault precedence family", lambda root: _overlay(root)
        ["faultPrecedenceControl"].__setitem__(
            "expectedFamily", "rejectionCause")),
    ("fault precedence cause", lambda root: _overlay(root)
        ["faultPrecedenceControl"].__setitem__(
            "expectedCause", "unsatisfiable")),
    ("claim E8 rejoin", lambda root: _overlay(root)["nonClaims"].remove(
        "no E8 rejoin")),
    ("semantic closure", lambda root: root["capabilityClosure"]
        ["semanticClosure"]["proofRefs"].pop()),
    ("lease reducer", lambda root: root["leaseProtocol"]
        ["normativeReducer"]["rules"].__setitem__(
            "release", "ignore pending expiry")),
    ("retained D9 row", lambda root: root["d9Derivation"]["rows"][1]
        ["expectedTermination"].__setitem__(
            "errorCode", "REQUEST.PRECONDITION_FAILED")),
]


TOTALITY_CASES: list[tuple[str, Any]] = [
    ("string root", "hostile"),
    ("null root", None),
    ("array root", []),
    ("empty root", {}),
]


def selftest(candidate: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    base = check(candidate)
    if base:
        return [
            f"REFUSING selftest: base candidate has {len(base)} finding(s): "
            f"{base[0]}"
        ]
    for label, mutate in MUTATIONS:
        changed = copy.deepcopy(candidate)
        before = canonical(changed)
        try:
            mutate(changed)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
            failures.append(
                f"mutation {label!r} failed to apply ({type(exc).__name__})")
            continue
        if canonical(changed) == before:
            failures.append(f"mutation {label!r} made no change")
            continue
        if not check(changed):
            failures.append(f"mutation escaped: {label}")
    for label, value in TOTALITY_CASES:
        try:
            findings = check(value)
        except Exception as exc:  # pragma: no cover - this is the assertion
            failures.append(
                f"totality {label!r} raised {type(exc).__name__}")
            continue
        if not findings:
            failures.append(f"hostile root escaped: {label}")
    return failures


def main(argv: list[str]) -> int:
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        candidate = load(path)
    except (OSError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError) as exc:
        print(f"cannot load RT14 candidate: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2
    if "--selftest" in argv[1:]:
        if not isinstance(candidate, dict):
            print("selftest requires an object root", file=sys.stderr)
            return 1
        failures = selftest(candidate)
        if failures:
            print(f"RT14 selftest: {len(failures)} failure(s)")
            for failure in failures:
                print("  -", failure)
            return 1
        print(
            f"PASS: RT14 selftest; {len(MUTATIONS)} mutations rejected; "
            f"{len(TOTALITY_CASES)} hostile roots rejected"
        )
        return 0
    findings = check(candidate)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    print(
        "PASS: retention-tiers.v14.json; exact RT13 projection; "
        "23 refs / 20 edges / 2 units; 11 retained D9 rows + 1 local "
        "unavailable row + 4 admitted CoreCompletion rows; D9 v1.8 "
        "candidate pinned, NOT-APPLIED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
